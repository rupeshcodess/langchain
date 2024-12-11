import streamlit as st
from groq import Groq
import shelve

st.title("TalkBot")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

# Set your API key directly in the code
api_key = "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"  # Replace this with your actual Groq API key

# Initialize Groq client with the API key
client = Groq(api_key=api_key)

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
        
        # Using Groq's Cloud API syntax for completions
        chat_completion = client.chat.completions.create(
            messages=[
                # Optional system message
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                # User message
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=st.session_state["groq_model"],
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )
        
        # Assuming the response is structured as in the example
        full_response = chat_completion.choices[0].message.content
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Save chat history after each interaction
save_chat_history(st.session_state.messages)
