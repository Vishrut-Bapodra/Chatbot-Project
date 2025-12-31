#App.py

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from backend.settings import chatbot_settings
from backend.chatbot_backend import get_chatbot_response
from backend.sidebar import sidebar_options
from backend.database import (
    init_db,
    get_all_chats,
    create_chat_session,
    load_chat_messages,
    save_message,
)

# --------------------------------------------------------------
# Initialize page and database
# --------------------------------------------------------------
st.set_page_config(page_title="UE.ai", layout="wide")
init_db()

# --------------------------------------------------------------
# CSS (unchanged)
# --------------------------------------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg,#0f2027, #203a43, #2c5634);
    color: #fff;
}
.chat-container {
    max-height: 75vh;
    overflow-y: scroll;
    padding:20px;
    border-radius: 15px;
    background:rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    margin-bottom: 1rem;
    border: 1px solid rgba(255,255,255,0.2);
}
.user-bubble {
    background: linear-gradient(90deg, #0078ff, #00c6ff);
    color: white;
    border-radius: 12px 12px 0 12px;
    padding:12px 16px;
    margin: 8px 0;
    max-width: 75%;
    float: right;
    clear: both;
}
.bot-bubble {
    background: linear-gradient(90deg, #444, #555);
    color: #e8e8e8;
    border-radius: 12px 12px 12px 0;
    padding: 12px 16px;
    margin: 8px 0;
    max-width: 75%;
    float: left;
    clear: both;
}
h1  {
    text-align: center;
    color: #e8e8e8;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------
# Session State Initialization
# --------------------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "active_chat" not in st.session_state:
    chats = get_all_chats()
    if len(chats) == 0:
        new_id = create_chat_session("Chat 1")
        st.session_state.active_chat = new_id
    else:
        st.session_state.active_chat = chats[0]["id"]
    st.session_state.chat_history = load_chat_messages(st.session_state.active_chat)

if "show_chats" not in st.session_state:
    st.session_state.show_chats = False

if "menu_open" not in st.session_state:
    st.session_state.menu_open = None

if "show_settings" not in st.session_state:
    st.session_state.show_settings = False

if "model_choice" not in st.session_state:
    st.session_state.model_choice = "openai/gpt-oss-120b"

st.title("💬 Chatbot")

# --------------------------------------------------------------
# Fallback after sidebar (handle active_chat == None)
# --------------------------------------------------------------
if st.session_state.active_chat is None:
    chats = get_all_chats()
    if len(chats) > 0:
        st.session_state.active_chat = chats[0]["id"]
        st.session_state.chat_history = load_chat_messages(st.session_state.active_chat)
    else:
        st.session_state.chat_history = []

# --------------------------------------------------------------
# Top Buttons (Settings / File Upload)
# --------------------------------------------------------------
col1, col2, col3, col4 = st.columns([4, 1, 1, 1])

with col3:
    if st.button("⚙ Settings", key="toggle_settings"):
        st.session_state.show_settings = not st.session_state.show_settings

with col4:
    if st.button("💬 Chats", key="toggle_chats"):
       st.session_state.show_chats = not st.session_state.get("show_chats", False)

# --------------------------------------------------------------
# Panels (Settings / File Upload)
# --------------------------------------------------------------
if st.session_state.show_settings:
    chatbot_settings()
    st.stop()
    
if st.session_state.show_chats:
    sidebar_options()

# --------------------------------------------------------------
# CHAT UI
# --------------------------------------------------------------

st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for chat in st.session_state.chat_history:
    bubble = "user-bubble" if chat["role"] == "user" else "bot-bubble"
    name = "🧑 You" if chat["role"] == "user" else "🤖 Bot"
    st.markdown(
        f"<div class='{bubble}'><b>{name}:</b> {chat['content']}</div>",
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------------------
# USER INPUT
# --------------------------------------------------------------
user_input = st.chat_input("Ask anything you want")

# user sends message
if user_input:
    st.session_state.pending_message = user_input  # save message to handle later
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    save_message(st.session_state.active_chat, "user", user_input)
    st.rerun()   


# handle bot response after UI refresh
if "pending_message" in st.session_state:

    pending = st.session_state.pending_message

    with st.empty():
        st.markdown(
            "<div style='color:#bbb; font-style:italic;'>Responding...</div>",
            unsafe_allow_html=True
        )

    # Call LLM
    bot_reply = get_chatbot_response(
        [{"role": "user", "content": pending}],
        model=st.session_state.model_choice
    )

    # Save bot reply
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
    save_message(st.session_state.active_chat, "assistant", bot_reply)

    # Clear pending state
    del st.session_state.pending_message

    st.rerun()


# Keep chat history synced
st.session_state.chat_history = load_chat_messages(st.session_state.active_chat)
