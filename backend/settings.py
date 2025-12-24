import streamlit as st

def chatbot_settings():
            st.title("⚙ Chatbot Settings")
            st.radio(
                "Choose Model:",
                [
                    "openai/gpt-oss-120b",
                    "qwen/qwen-2.5-72b-instruct:free",
                    "deepseek/deepseek-r1-0528-qwen3-8b:free",
                    "kwaipilot/kat-coder-pro:free",
                    "meta-llama/llama-3.1-8b-instruct",
                    "mistralai/mistral-7b-instruct",
                    "google/gemma-7b-it"
                ],
                key="model_choice"
            )
            st.slider("Creativity",0.0,1.5,0.7,key="temperature")
            if st.button("🧹 Clear chat"):
                st.session_state.chat_history = []