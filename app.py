import streamlit as st
import requests
import os

st.set_page_config(
    page_title="Finance AI Assistant",
    page_icon="📊",
    layout="wide"
)

API_BASE_URL = "http://127.0.0.1:8000/api/v1"

st.title("📊 Finance AI Knowledge System")

with st.sidebar:
    st.header("📄 Document Indexing")

    uploaded_files = st.file_uploader(
        "Upload Finance PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("Process & Index"):
        if uploaded_files:
            files_payload = [
                ("files", (f.name, f.read(), "application/pdf"))
                for f in uploaded_files
            ]

            response = requests.post(
                f"{API_BASE_URL}/upload",
                files=files_payload
            )

            if response.status_code == 200:
                st.success("Documents indexed successfully!")
            else:
                st.error("Failed to index documents.")

st.divider()

if prompt := st.chat_input("Ask a financial question..."):

    st.chat_message("user").write(prompt)

    try:
        response = requests.post(
            f"{API_BASE_URL}/query",
            json={"question": prompt}
        )

        if response.status_code == 200:
            answer = response.json()["answer"]
            st.chat_message("assistant").write(answer)
        else:
            st.error("Backend returned an error.")

    except Exception as e:
        st.error(f"Connection Error: {e}")
