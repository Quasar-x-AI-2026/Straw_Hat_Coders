import streamlit as st
import json
from pathlib import Path
from gradio_client import Client

SPACE_ID = "Priyanshu292004/chatbot-mental-new"
client = Client(SPACE_ID)

BASE_DIR = Path(__file__).resolve().parent
context_file = BASE_DIR / "context.json"

st.set_page_config(page_title="Mental Health Insight Chatbot")
st.title("🧠 Mental Health Insight Chatbot")

if context_file.exists():
    with open(context_file) as f:
        context = json.load(f)

    st.subheader("Reflection Prompt")
    st.info(context["reflection_prompt"])

    with st.spinner("Analyzing your mental health data..."):
        response = client.predict(
            json.dumps(context),
            api_name="/chat"
        )

    st.subheader("AI Insight")
    st.write(response)
else:
    st.warning("No context provided from dashboard.")

st.divider()

# ---- Chat continuation ----
if "messages" not in st.session_state:
    st.session_state.messages = []

for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.write(msg)

user_input = st.chat_input("Continue the conversation...")

if user_input:
    st.session_state.messages.append(("user", user_input))
    with st.chat_message("assistant"):
        reply = client.predict(user_input, api_name="/chat")
        st.write(reply)
        st.session_state.messages.append(("assistant", reply))
