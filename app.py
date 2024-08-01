import os
import json

import streamlit as st
from groq import Groq

st.set_page_config(
  page_title='Yantriki',
  page_icon=" 🤖",
  layout='centered'
)

try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    base_dir = os.getcwd()  # Fallback to the current working directory

# Define the relative path to the config file
config_file_path = os.path.join(base_dir, 'config.json')
try:
    with open(config_file_path, 'r') as config_file:
        config_data = json.load(config_file)
        # Access the API key from the loaded config data
        GROQ_API_KEY = config_data['GROQ_API_KEY']
        print("Config data loaded successfully.")
except FileNotFoundError:
    print(f"Error: {config_file_path} not found.")
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from {config_file_path}.")
except KeyError:
    print(f"Error: 'GROQ_API_KEY' not found in the config file.")

os.environ['GROQ_API_KEY'] = GROQ_API_KEY
client = Groq()


# initiallising the chat history as streamlit session state as not present already

if 'chat_history' not in st.session_state:
  st.session_state.chat_history = []
  
# streamlit page title
st.title('🤖 Yantriki: Your Personal Assistant')

#display chat history
for message in st.session_state.chat_history:
  with st.chat_message(message['role']):
    st.markdown(message['content'])
    
# input field for user message
user_prompt = st.chat_input("ASK LLAMA...")

if user_prompt:
  st.chat_message("user").markdown(user_prompt)
  st.session_state.chat_history.append({'role':'user','content': user_prompt})
  
  # sens user's message to the LLm and get the response
  messages=[
    {'role':'system','content':'You are a helpful assistant'},
    *st.session_state.chat_history
  ]
  
  response = client.chat.completions.create(
    model='llama-3.1-8b-instant',
    messages=messages
  )
  
  assistant_response = response.choices[0].message.content
  st.session_state.chat_history.append({'role':'assistant','content':assistant_response})
  
  with st.chat_message('assistant'):
    st.markdown(assistant_response)
