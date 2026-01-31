import streamlit as st
from gradio_client import Client

# =========================
# CONFIG
# =========================
SPACE_ID = "Priyanshu292004/chatbot-mental-new"  # <-- change this

client = Client(SPACE_ID)

# =========================
# STREAMLIT UI SETUP
# =========================
st.set_page_config(page_title="Mental Health Support Chatbot")
st.title("🧠 Mental Health Support Chatbot")
st.caption("This tool offers emotional support, not professional therapy.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for role, message in st.session_state.messages:
    with st.chat_message(role):
        st.write(message)

# User input
user_input = st.chat_input("Share what’s on your mind...")

if user_input:
    # Show user message
    st.session_state.messages.append(("user", user_input))
    with st.chat_message("user"):
        st.write(user_input)

    # Call Hugging Face Space API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.predict(
                    user_input,
                    api_name="/chat"
                )
                st.write(response)
                st.session_state.messages.append(("assistant", response))
            except Exception as e:
                st.error("The chatbot is currently unavailable. Please try again.")
