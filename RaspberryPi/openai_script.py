import os
import openai

openai.api_key = os.environ.get('OPENAI_API_KEY')

def run_command_openai(prompt):
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "user", "content": prompt},
        ]
    )
    
    text_response = completion['choices'][0]['message']['content'].strip()
    print(text_response)
    return text_response


