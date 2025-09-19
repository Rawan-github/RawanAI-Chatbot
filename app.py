import streamlit as st
import time
import requests
import uuid
from datetime import datetime
import PyPDF2
import docx
import pandas as pd

# =====================
# Page Configuration
# =====================
st.set_page_config(
    page_title="RawanAI Chatbot",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="expanded",
)

# =====================
# Custom CSS
# =====================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif !important;
    }

    .header {
        background: linear-gradient(90deg, #8E2DE2, #4A00E0);
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 2rem;
    }

    .user-bubble {
        background-color: #0078FF;
        color: white;
        padding: 10px 14px;
        border-radius: 18px 18px 4px 18px;
        margin: 6px 0;
        max-width: 80%;
        float: right;
        clear: both;
        word-wrap: break-word;
    }
    .ai-bubble {
        background-color: #2C2F38;
        color: #EAEAEA;
        padding: 10px 14px;
        border-radius: 18px 18px 18px 4px;
        margin: 6px 0;
        max-width: 80%;
        float: left;
        clear: both;
        word-wrap: break-word;
        opacity: 0;
        animation: fadeIn 0.6s ease forwards;
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    .timestamp {
        font-size: 0.7rem;
        margin-top: 4px;
        display: block;
    }
    .user-time {
        text-align: right;
        color: #ccc;
    }
    .ai-time {
        text-align: left;
        color: #aaa;
    }

    .footer {
        margin-top: 2rem;
        text-align: center;
        color: #777;
        font-size: 0.85rem;
    }

    /* Spacing fixes */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    .stTextInput, .stTextArea, .stFileUploader {
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================
# Header
# =====================
st.markdown('<div class="header">RawanAI Assistant</div>', unsafe_allow_html=True)

# =====================
# Session State
# =====================
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "saved_chats" not in st.session_state:
    st.session_state.saved_chats = {}

if "file_context" not in st.session_state:
    st.session_state.file_context = ""  # store uploaded file text

# =====================
# Sidebar 
# =====================
with st.sidebar:
    st.title("🗂️ Chat History")

    if "saved_chats" not in st.session_state:
        st.session_state.saved_chats = {}

    # Automatically save current chat under a name (if messages exist)
    if st.session_state.messages:
        first_msg = st.session_state.messages[0]["content"]
        chat_name = (first_msg[:30] + "...") if len(first_msg) > 30 else first_msg
        st.session_state.saved_chats[chat_name] = st.session_state.messages.copy()

    # Show saved chats in sidebar
    if st.session_state.saved_chats:
        for name in list(st.session_state.saved_chats.keys()):
            if st.button(f"💬 {name}"):
                st.session_state.messages = st.session_state.saved_chats[name].copy()
                st.success(f"Loaded chat: {name}")

    st.write("---")
    if st.button("🆕 New Chat"):
        st.session_state.messages = []
        st.success("Started a new conversation")

# Fixed backend URL
backend_host = "http://127.0.0.1:8000"

# =====================
# Chat Display
# =====================
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        time_sent = message.get("time", "")
        if role == "user":
            st.markdown(
                f'<div class="user-bubble">{content}<span class="timestamp user-time">{time_sent}</span></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="ai-bubble">{content}<span class="timestamp ai-time">{time_sent}</span></div>',
                unsafe_allow_html=True,
            )

# =====================
# Chat Input
# =====================
prompt = st.chat_input("Type your message here...")

if prompt:
    now = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({"role": "user", "content": prompt, "time": now})
    st.markdown(
        f'<div class="user-bubble">{prompt}<span class="timestamp user-time">{now}</span></div>',
        unsafe_allow_html=True,
    )

    placeholder = st.empty()
    for _ in range(2):
        for dots in ["", ".", "..", "..."]:
            placeholder.markdown(
                f'<div class="ai-bubble">RawanAI is typing{dots}<span class="timestamp ai-time">{datetime.now().strftime("%H:%M")}</span></div>',
                unsafe_allow_html=True,
            )
            time.sleep(0.4)

    try:
        resp = requests.post(
            backend_host.rstrip("/") + "/chat",
            json={
                "prompt": prompt,
                "session_id": st.session_state.session_id,
                "context": st.session_state.file_context,  # include uploaded file text
            },
            timeout=20,
        )
        if resp.status_code == 200:
            answer = resp.json().get("answer", "⚠️ No response")
        else:
            answer = f"❌ API Error ({resp.status_code})"
    except Exception as e:
        answer = f"⚠️ Could not connect to backend: {e}"

    now = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({"role": "assistant", "content": answer, "time": now})
    placeholder.markdown(
        f'<div class="ai-bubble">{answer}<span class="timestamp ai-time">{now}</span></div>',
        unsafe_allow_html=True,
    )

# =====================
# File Upload Section 
# =====================
st.subheader("📂 Upload a File")
uploaded_file = st.file_uploader("Attach a file to enrich the conversation", type=["txt", "pdf", "docx", "csv"])
if uploaded_file:
    text_data = ""
    if uploaded_file.type == "text/plain":
        text_data = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            text_data += page.extract_text() or ""
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text_data += para.text + "\n"
    elif uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
        text_data = df.to_string()

    st.session_state.file_context = text_data
    st.success(f"✅ File {uploaded_file.name} is now attached to your chat!")
    st.caption("Any questions you ask will now consider this file’s content.")

# =====================
# Footer
# =====================
st.markdown('<div class="footer">© 2025 RawanAI — Powered by Cohere</div>', unsafe_allow_html=True)
