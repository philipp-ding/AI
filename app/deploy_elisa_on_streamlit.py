"""
# My first app
Here's our first attempt at using data to create a table:

Deployment:
Share your app

After you’ve built a Streamlit app, it's time to share it! To show it off to the world you can use Streamlit Community Cloud to deploy, manage, and share your app for free.

It works in 3 simple steps:

    Put your app in a public GitHub repo (and make sure it has a requirements.txt!)
    Sign into share.streamlit.io
    Click 'Deploy an app' and then paste in your GitHub URL

That's it! 🎈 You now have a publicly deployed app that you can share with the world. Click to learn more about how to use Streamlit Community Cloud.
"""

import streamlit as st
import time
from streamlit_chat import message
import logging
import sys
sys.path.append('..')
from src.ELIZA_chatbot import respond_external

st.header("Weizenabaums ELIZA chatbot")
st.markdown("[Github](https://github.com/ai-yash/st-chat)")

if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Hello. How are you feeling today?"]

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'text' not in st.session_state:
    st.session_state['text'] = ""

def clear_text():
    # st.session_state["text"] = ""
    st.session_state["temp"] = ""

def clear_text_after_input():
    st.session_state["temp"] = st.session_state["text"]
    st.session_state["text"] = ""

def clear_conversation():
    clear_text()
    st.session_state['generated'] = ["Hello. How are you feeling today?"]
    st.session_state['past'] = []

input_text = st.text_input("Write something... ", key="text", on_change=clear_text_after_input())
user_input = st.session_state["temp"]

st.button("clear conversation", on_click=clear_conversation)

if user_input:
    output = respond_external(user_input)
    st.session_state.generated.append(output)
    st.session_state.past.append(user_input)
    user_input = ""

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        if i > 0:
            message(st.session_state['past'][i-1], is_user=True, key=str(i-1) + '_user')
