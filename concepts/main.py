import streamlit as st
import requests
from dotenv import load_dotenv
import os


#web-page setup
st.set_page_config(page_title="AI chatbot", page_icon="💬")
st.title("💬 AI chatbot")

#loading the api key
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    st.error("API key not found")
    st.stop()

#chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

#user input field
user_input = st.text_input("Enter your message:")

#Send button setup
if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please enter a message first.")
    else:
        #adding user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        payload = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": st.session_state.chat_history,
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "AI chatbot"
        }

        #Try block
        try:
            #sending prompt to openai through api key
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )
            data = response.json()


            #displaying bot reply
            if "choices" in data:
                bot_reply = data["choices"][0]["message"]["content"]

                #Adding bot's reply to history
                st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
            else:
                st.error(f"Unexpected response: {data}")


        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
        
#Displaying chat history
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"**👨 You:** {chat['content']}")
    else:
        st.markdown(f"**🤖 Bot:** {chat['content']}")