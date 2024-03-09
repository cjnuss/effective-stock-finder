import requests
import os
from openai import OpenAI
from dotenv import load_dotenv

#Loads the env file and gets the key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

#OpenAI requests 
client = OpenAI()
def process_input(prompt):
    try:
        user_input = input("You: ")
        prompt += f"You: {user_input}\n"
        gpt_response = client.chat.completions.create(model="gpt-4",
            messages=[{"role": "system", "content": prompt}])
        content = gpt_response.choices[0].message.content
        print(content)
        return f"{prompt}{content}\n"
    except Exception as e:
        print(f"Error from OpenAI API: {e}")
        return prompt


prompt = "You are a helpful assistant."
#Needs modification 
while True:
    prompt = process_input(prompt)