import streamlit as st
from dotenv import load_dotenv
import os
import shelve
from groq import Groq
import apikey  # Assuming this contains your API key

# Load environment variables
load_dotenv()

st.title("TalkBot")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

# Initialize Groq client
client = Groq(api_key="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")

# Ensure groq_model is initialized in session state
if "groq_model" not in st.session_state:
    st.session_state["groq_model"] = "llama3-8b-8192"

# Load chat history from shelve file
def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])

# Save chat history to shelve file
def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages

# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# Sidebar with a button to delete chat history
with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Main chat interface
if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        chat_completion = client.completions.create(
            model=st.session_state["groq_model"],
            messages=st.session_state["messages"] + [{"role": "user", "content": prompt}],
        )
        for response in chat_completion.choices:
            full_response += response.message.content
            message_placeholder.markdown(full_response + "|")
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Save chat history after each interaction
save_chat_history(st.session_state.messages)

