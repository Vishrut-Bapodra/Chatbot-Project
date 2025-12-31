import streamlit as st
from backend.chatbot_backend import get_chatbot_response

st.set_page_config(page_title="AI Chatbot 💬")

st.markdown("""
    <style>
    .user-bubble {
        background-color:#eb3b38;
        border-radius: 15px;
        padding: 10px;
        margin: 5px 0;
        max-width: 80%;
        float: right;
        clear: both;
    }
    .bot-bubble {
        background-color:#dfeb38;
        border-radius: 15px;
        padding: 10px;
        margin: 5px 0;
        max-width: 80%;
        float: left;
        clear: both;           
    }
    .chat-container {
        max-height: 70vh;
        overflow-y: auto;
        padding: 10px;
        border-radius: 10px;
        background-color: #38c1eb;            
    }
    </style>
""",unsafe_allow_html=True)

#SIDEBAR SETTTINGS
st.sidebar.title("⚙ Settings")
model_choice = st.sidebar.radio(
    "Choose Model:",
    ["mistralai/mistral-7b-instruct","meta-llama/llama-3.1-8b-instruct", "google/gemma-7b-it"]
)
temperature = st.sidebar.slider("Creativity",0.0,1.5,0.7)
if st.sidebar.button("🚮 clear chat"):
    st.session_state.chat_history = []
    st.rerun()

#DISPLAYING CHAT HISTORY
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
st.title("AI Chatbot 💬")

#DISPLAY AREA FOR CHAT HISTORY
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"<div class='user-bubble'> 🧑 You: {chat['content']}")
    else:
        st.markdown(f"<div class='bot-bubble'> 🤖 Bot: {chat['content']}")
st.markdown('</div>',unsafe_allow_html=True)

#USER INPUT
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask whatever you want to ask", key="input_field")
    send = st.form_submit_button("send")
if send:
    if user_input.strip() == "":
        st.warning("Please enter a message fot it to be processed.")
    else:
        st.session_state.chat_history.append({"role" : "user", "content" : user_input})
        try:
            bot_reply = get_chatbot_response(
                [{"role": "user", "content": user_input}],
                model=model_choice,
                temperature=temperature
            )

            st.session_state.chat_history.append({"role":"assistant","content": bot_reply})
        except Exception as e:
            st.error(f"Error:{e}")
        st.rerun()