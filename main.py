from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langchain_cohere import ChatCohere
from langchain.schema import HumanMessage, AIMessage
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# FastAPI
app = FastAPI(title="RawanAI API", version="1.1")

# Allow CORS (Streamlit frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# Schemas
class ChatRequest(BaseModel):
    prompt: str
    session_id: str
    context: str | None = None

class ChatResponse(BaseModel):
    answer: str

# Initialize Cohere LLM
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise ValueError("⚠️ Missing COHERE_API_KEY")

llm = ChatCohere(
    cohere_api_key=COHERE_API_KEY,
    model="command-a-03-2025"
)

# In-memory chat history
chat_histories = {}

@app.get("/health")
async def health():
    return {"status": "ok", "model": "Cohere command-a-03-2025"}

@app.post("/chat", response_model=ChatResponse)
async def chat_with_cohere(request: ChatRequest):
    if not request.prompt or not request.session_id:
        raise HTTPException(status_code=400, detail="prompt and session_id are required")

    effective_prompt = request.prompt
    if request.context:
        effective_prompt = f"{request.prompt}\n\n[File context:]\n{request.context[:2000]}"

    history = chat_histories.get(request.session_id, [])
    history.append(HumanMessage(content=effective_prompt))
    response = llm.invoke(history)
    history.append(AIMessage(content=response.content))
    chat_histories[request.session_id] = history

    return ChatResponse(answer=response.content)
