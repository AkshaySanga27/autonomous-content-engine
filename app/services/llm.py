import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()

def get_llm():
    key=os.getenv('GOOGLE_API_KEY')
    if not key: raise RuntimeError('GOOGLE_API_KEY is missing. Copy .env.example to .env and add your key.')
    return ChatGoogleGenerativeAI(model=os.getenv('LLM_MODEL','gemini-2.0-flash'), temperature=0.4)
