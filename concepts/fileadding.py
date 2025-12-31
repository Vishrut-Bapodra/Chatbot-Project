import streamlit as st
import os

UPLOAD_DIR = "uploaded_files"

os.makedirs(UPLOAD_DIR, exist_ok=True)

def file_uploading_button():
    if st.session_state.show_file_panel:
        st.title("📁 Upload File")

        uploaded_file = st.file_uploader(
            "Upload any file",
            type=["txt", "pdf", "docx", "csv", "json"]
        )

        if uploaded_file:
            file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

            # save file to disk
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # store saved path for backend use
            st.session_state.last_uploaded_file_path = file_path

            st.success(f"File '{uploaded_file.name}' saved and ready to read!")

        if st.button("Close File panel"):
            st.session_state.show_file_panel = False
