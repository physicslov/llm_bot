import os
import json

import streamlit as st
from groq import Groq

st.set_page_config(
  page_title='Yantriki',
  page_icon=" 🤖",
  layout='centered'
)

config_data = json.load(open('C:/Users/physi/OneDrive/Desktop/pyrh/config.json'))
GROQ_API_KEY=  config_data['GROQ_API_KEY']
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