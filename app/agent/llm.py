import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

load_dotenv()

_current_provider = "gemini"

def set_llm_provider(provider: str):
    global _current_provider
    _current_provider = provider.lower()

def get_llm(temperature: float = 0.7, provider: str = None):
    use_provider = provider or _current_provider
    
    if use_provider == "gemini":
        return ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=temperature)
    else:
        return ChatOllama(model="gpt-oss:20b", temperature=temperature)

llm = get_llm()

def get_response_content(response):
    if hasattr(response, 'content'):
        return response.content
    return str(response)

