import os
import logging
import json

import click
import sounddevice as sd
import google.oauth2.credentials
import google.auth.transport.grpc
import google.auth.transport.requests

from google.assistant.embedded.v1alpha2 import (
    embedded_assistant_pb2,
    embedded_assistant_pb2_grpc
)

try:
    from . import (
        assistant_helpers,
        audio_helpers,
        browser_helpers,
    )
except (SystemError, ImportError):
    import assistant_helpers
    import audio_helpers
    import browser_helpers


ASSISTANT_API_ENDPOINT = 'embeddedassistant.googleapis.com'
DEFAULT_GRPC_DEADLINE = 60 * 3 + 5
PLAYING = embedded_assistant_pb2.ScreenOutConfig.PLAYING

class GoogleAssistant(object):
    def __init__(self, language_code, device_model_id, device_id,
                 display, channel, deadline_sec):
        self.language_code = language_code
        self.device_model_id = device_model_id
        self.device_id = device_id
        self.conversation_state = None
        self.is_new_conversation = True
        self.display = display
        self.assistant = embedded_assistant_pb2_grpc.EmbeddedAssistantStub(channel)
        self.deadline = deadline_sec

    def __enter__(self):
        return self

    def __exit__(self, etype, e, traceback):
        if e:
            return False

    def assist(self, text_query):
        def iter_assist_requests():
            config = embedded_assistant_pb2.AssistConfig(
                audio_out_config=embedded_assistant_pb2.AudioOutConfig(
                    encoding='LINEAR16',
                    sample_rate_hertz=16000,
                    volume_percentage=0,
                ),
                dialog_state_in=embedded_assistant_pb2.DialogStateIn(
                    language_code=self.language_code,
                    conversation_state=self.conversation_state,
                    is_new_conversation=self.is_new_conversation,
                ),
                device_config=embedded_assistant_pb2.DeviceConfig(
                    device_id=self.device_id,
                    device_model_id=self.device_model_id,
                ),
                text_query=text_query,
            )
            self.is_new_conversation = False
            if self.display:
                config.screen_out_config.screen_mode = PLAYING
            req = embedded_assistant_pb2.AssistRequest(config=config)
            assistant_helpers.log_assist_request_without_audio(req)
            yield req
        
        #configured conversation stream
        audio_device = None
        audio_source = audio_device = (
            audio_device or audio_helpers.SoundDeviceStream(
                sample_rate=audio_helpers.DEFAULT_AUDIO_SAMPLE_RATE,
                sample_width=audio_helpers.DEFAULT_AUDIO_SAMPLE_WIDTH,
                block_size=audio_helpers.DEFAULT_AUDIO_DEVICE_BLOCK_SIZE,
                flush_size=audio_helpers.DEFAULT_AUDIO_DEVICE_FLUSH_SIZE
            )
        )
        audio_sink = audio_device = (
        audio_device or audio_helpers.SoundDeviceStream(
                sample_rate=audio_helpers.DEFAULT_AUDIO_SAMPLE_RATE,
                sample_width=audio_helpers.DEFAULT_AUDIO_SAMPLE_WIDTH,
                block_size=audio_helpers.DEFAULT_AUDIO_DEVICE_BLOCK_SIZE,
                flush_size=audio_helpers.DEFAULT_AUDIO_DEVICE_FLUSH_SIZE
            )
        )
        conversation_stream = audio_helpers.ConversationStream(
            source=audio_source,
            sink=audio_sink,
            iter_size=audio_helpers.DEFAULT_AUDIO_ITER_SIZE,
            sample_width=audio_helpers.DEFAULT_AUDIO_SAMPLE_WIDTH,
        )
    
        text_response = None
        html_response = None
        for resp in self.assistant.Assist(iter_assist_requests(),
                                          self.deadline):
            assistant_helpers.log_assist_response_without_audio(resp)
            if resp.screen_out.data:
                html_response = resp.screen_out.data
            if resp.dialog_state_out.conversation_state:
                conversation_state = resp.dialog_state_out.conversation_state
                self.conversation_state = conversation_state
            if resp.dialog_state_out.supplemental_display_text:
                text_response = resp.dialog_state_out.supplemental_display_text
                
            #added sound output
            if len(resp.audio_out.audio_data) > 0:
                if not conversation_stream.playing:
                    conversation_stream.stop_recording()
                    conversation_stream.start_playback()
                    print('Playing assistant response.....')
                conversation_stream.write(resp.audio_out.audio_data)
                
        conversation_stream.stop_playback()
        return text_response, html_response

@click.command()
@click.option('--command',
              metavar='<command>',
              required=True,
              help=('Command entered by the user'))
@click.option('--api-endpoint', default=ASSISTANT_API_ENDPOINT,
              metavar='<api endpoint>', show_default=True,
              help='Address of Google Assistant API service.')
@click.option('--credentials',
              metavar='<credentials>', show_default=True,
              default=os.path.join(click.get_app_dir('google-oauthlib-tool'),
                                   'credentials.json'),
              help='Path to read OAuth2 credentials.')
@click.option('--device-model-id',
              metavar='<device model id>',
              required=True,
              help=(('Unique device model identifier, '
                     'if not specifed, it is read from --device-config')))
@click.option('--device-id',
              metavar='<device id>',
              required=True,
              help=(('Unique registered device instance identifier, '
                     'if not specified, it is read from --device-config, '
                     'if no device_config found: a new device is registered '
                     'using a unique id and a new device config is saved')))
@click.option('--lang', show_default=True,
              metavar='<language code>',
              default='en-US',
              help='Language code of the Assistant')
@click.option('--display', is_flag=True, default=False,
              help='Enable visual display of Assistant responses in HTML.')
@click.option('--verbose', '-v', is_flag=True, default=False,
              help='Verbose logging.')
@click.option('--grpc-deadline', default=DEFAULT_GRPC_DEADLINE,
              metavar='<grpc deadline>', show_default=True,
              help='gRPC deadline in seconds')
def main(command, api_endpoint, credentials,
         device_model_id, device_id, lang, display, verbose,
         grpc_deadline, *args, **kwargs):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

    try:
        with open(credentials, 'r') as f:
            credentials = google.oauth2.credentials.Credentials(token=None,
                                                                **json.load(f))
            http_request = google.auth.transport.requests.Request()
            credentials.refresh(http_request)
    except Exception as e:
        logging.error('Error loading credentials: %s', e)
        logging.error('Run google-oauthlib-tool to initialize '
                      'new OAuth 2.0 credentials.')
        return

    grpc_channel = google.auth.transport.grpc.secure_authorized_channel(
        credentials, http_request, api_endpoint)

    with GoogleAssistant(lang, device_model_id, device_id, display,
                             grpc_channel, grpc_deadline) as assistant:
        response_text, response_html = assistant.assist(text_query=command)
        if display and response_html:
            system_browser = browser_helpers.system_browser
            system_browser.display(response_html)
        if response_text:
            print(f'Transcript of response: {response_text}')

if __name__ == '__main__':
    main()