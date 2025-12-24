# 🤖 Chatbot Project

A conversational AI chatbot built with **Streamlit** as the frontend UI and integrated with the **OpenRouter API** for large language model responses. It offers session management, message history stored in SQLite, and an interactive interface to chat with AI.

---

## 🧠 Project Overview

This project provides an intuitive chat interface enabling users to interact with an AI model in real time. The backend calls the OpenRouter API to generate AI responses, and the app stores all conversations locally in a SQLite database. The UI also includes panels for chat session management and settings such as model selection and temperature, though these settings are currently static placeholders.

---

## ✨ Key Features

- 🗨️ **Interactive Chat Interface:** Built using Streamlit to handle user messages and display AI replies.
- 💬 **Chat Session Management:** Create, rename, and delete chat sessions.
- 💾 **Persistent Storage:** Uses SQLite to store chat history across multiple sessions.
- ⚙️ **Settings Panel:** UI controls for model choice and temperature (currently static).
- 🔎 **Optional Tool Support:** Includes logic for tool calls like web search when supported by the model.
- 🌱 **Clean UI Design:** Modern layout with sidebar controls and styled message bubbles.

---

## 🛠️ Built With

| Technology | Description |
|------------|-------------|
| **Python 3.x** | Core language |
| **Streamlit** | Frontend UI |
| **SQLite** | Local database for chat history |
| **OpenRouter API** | Language model responses |
| **Requests** | HTTP calls to external APIs |
| **python-dotenv** | Environment variable handling |

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.8+
- Git
- OpenRouter API Key
- (Optional) Serper API Key for web search

---

### 📥 Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/Vishrut-Bapodra/Chatbot-Project.git
    cd Chatbot-Project
    ```

2. **Set up a virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate      # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

---

### ⚙️ Configuration

Create a `.env` file in the project root with your API keys:
