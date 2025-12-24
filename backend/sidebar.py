import streamlit as st
from database import (
    get_all_chats,
    create_chat_session,
    load_chat_messages,
    delete_chat,
    rename_chat
)

# ============================
# STREAMLIT DIALOGS
# ============================

@st.dialog("Rename Chat")
def rename_dialog(chat_id, old_name):
    new_name = st.text_input("Enter new name:", value=old_name, key=f"rename_input_{chat_id}")
    if st.button("Save"):
        rename_chat(chat_id, new_name)
        st.rerun()

    if st.button("Cancel"):
        st.rerun()


@st.dialog("Delete Chat")
def delete_dialog(chat_id):
    st.error("Are you sure you want to delete this chat permanently?")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Yes, delete"):
            delete_chat(chat_id)
            st.rerun()

    with col2:
        if st.button("Cancel"):
            st.rerun()


# ============================
# SIDEBAR OPTIONS
# ============================
def sidebar_options():

    sidebar_container = st.sidebar.container()
    with sidebar_container:
        st.header("💬 Chats")

        chats = get_all_chats()

        st.markdown("""
            <style>
            .chat-row button {
                padding: 4px 8px !important;
                font-size: 14px !important;
            }
            .menu-btn { 
                visibility: hidden; 
                float: right; 
                margin-right: 5px; 
            }
            .chat-row:hover .menu-btn { 
                visibility: visible; 
            }
            </style>
        """, unsafe_allow_html=True)


        for chat in chats:
            chat_id = chat["id"]
            chat_name = chat["name"]

            st.markdown("<div class='chat-row'>", unsafe_allow_html=True)
            col1, col2 = st.columns([5, 1])

            # Select chat
            with col1:
                if st.button(chat_name, key=f"select_{chat_id}"):
                    st.session_state.active_chat = chat_id
                    st.session_state.chat_history = load_chat_messages(chat_id)
                    st.rerun()

            # Three-dots menu
            with col2:
                if st.button("⋮", key=f"menu_{chat_id}", help="Options"):
                    st.session_state.menu_open = chat_id if st.session_state.get("menu_open") != chat_id else None

            st.markdown("</div>", unsafe_allow_html=True)

            # Show menu under the chat
            if st.session_state.get("menu_open") == chat_id:
                rcol, dcol = st.columns(2)

                # RENAME
                with rcol:
                    if st.button("✏️ Rename", key=f"rename_btn_{chat_id}"):
                        old_name = chat_name
                        rename_dialog(chat_id, old_name)

                # DELETE
                with dcol:
                    if st.button("🗑️ Delete", key=f"delete_btn_{chat_id}"):
                        delete_dialog(chat_id)

        # New Chat button
        if st.button("➕ New Chat"):
            new_id = create_chat_session("New Chat")
            st.session_state.active_chat = new_id
            st.session_state.chat_history = []
            st.rerun()
