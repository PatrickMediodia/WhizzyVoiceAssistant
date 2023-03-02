import os
import openai

openai.api_key = os.environ.get('OPENAI_API_KEY')

def run_command_openai(prompt):
    completion = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    return completion.choices[0].text
