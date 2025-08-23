import streamlit as st
import requests
from uuid import uuid4

st.set_page_config(page_title="Claude Sonnet RAG Chatbot", page_icon="🤖")

# Session state setup 
if "chats" not in st.session_state:
    st.session_state.chats = {}  # {chat_id: {"name": str, "messages": list}}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None


# Sidebar: Chat Manager 
st.sidebar.title("💬 Chat Sessions")

# Create a new chat
if st.sidebar.button("➕ New Chat"):
    chat_id = str(uuid4())[:8]  # short random id
    st.session_state.chats[chat_id] = {"name": f"Chat {len(st.session_state.chats)+1}", "messages": []}
    st.session_state.current_chat = chat_id

# List existing chats
for chat_id, chat in list(st.session_state.chats.items()):
    col1, col2 = st.sidebar.columns([3,1])
    if col1.button(chat["name"], key=f"select_{chat_id}"):
        st.session_state.current_chat = chat_id
    if col2.button("🗑️", key=f"delete_{chat_id}"):
        del st.session_state.chats[chat_id]
        if st.session_state.current_chat == chat_id:
            st.session_state.current_chat = None

# Main Chat Window
st.title("Claude Sonnet Chatbot (with Knowledge Base)")

if st.session_state.current_chat is None:
    st.info("👉 Create or select a chat from the sidebar to get started.")
else:
    chat = st.session_state.chats[st.session_state.current_chat]

    # Input box
    query = st.text_input("Ask me something:", key="chat_input")

    if st.button("Send") and query:
        with st.spinner("Thinking..."):
            response = requests.post(
                "http://backend:8000/chat",
                json={"query": query},
                stream=True
            )

            collected = ""
            placeholder = st.empty()

            for chunk in response.iter_lines():
                if chunk:
                    token = chunk.decode("utf-8")
                    collected += token
                    placeholder.markdown(f"**Claude:** {collected}")

            # Save to history
            chat["messages"].append({"role": "user", "content": query})
            chat["messages"].append({"role": "claude", "content": collected})

    # Display history
    st.subheader(chat["name"])
    for msg in chat["messages"]:
        if msg["role"] == "user":
            st.markdown(f"🧑 **You:** {msg['content']}")
        else:
            st.markdown(f"🤖 **Claude:** {msg['content']}")
