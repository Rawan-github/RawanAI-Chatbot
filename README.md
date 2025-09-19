# 🤖 RawanAI ChatBot 💬

A chatbot built with FastAPI (backend) and Streamlit (frontend), powered by LangChain + Cohere.
It supports session-based memory so conversations flow naturally and can utilize uploaded files for context.

---

## 📂 Project Structure

```
├── main.py        # FastAPI backend (chat API with Cohere)
├── app.py         # Streamlit frontend (chat UI)
├── requirements.txt
└── README.md
```

---

## 🚀 Features

* ✅ FastAPI backend for chat requests
* ✅ Streamlit chat interface with modern UI
* ✅ Session-based conversation history
* ✅ Secure API key handling using `.env` (locally) or Streamlit Secrets (cloud)
* ✅ Powered by LangChain Cohere (command-a-03-2025 model)
* ✅ File upload support (.txt, .pdf, .docx, .csv) to enrich context

---

## 🛠️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/Rawan-github/rawanai-chatbot.git
cd rawanai-chatbot/streamlit
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API key

Create a `.env` file in the `streamlit/` folder:

```
COHERE_API_KEY=your_cohere_api_key_here
```

---

## ▶️ Running the Project

### Start FastAPI (Backend)

```bash
uvicorn main:app --reload --port 8000
```

* Runs the API at: `http://127.0.0.1:8000/chat`

### Start Streamlit (Frontend)

Open a **new terminal**:

```bash
streamlit run app.py
```

* Opens the chatbot UI in your browser.
* Example Streamlit Cloud URL (once deployed):

```
https://rawanai-chatbot-hqzmtjfjx9xjs6uxuatcj8.streamlit.app/
```

---

## 🌐 Deployment

* **Streamlit Cloud** → Deploy `app.py` (frontend). Use Secrets Manager for API key.
* **Railway / Render / Heroku** → Deploy `main.py` (backend).
* Optionally, host **backend + frontend separately** for production.

---

## 📜 License

This project is for **educational/demo purposes**. Feel free to fork and extend it!
