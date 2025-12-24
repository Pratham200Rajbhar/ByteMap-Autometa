import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

load_dotenv()

def get_llm(temperature: float = 0.7):
    """
    Easily switch between LLMs by commenting/uncommenting the return statements below.
    """
    
    # Switch by commenting/uncommenting these lines:
    # return ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=temperature)
    return ChatOllama(model="gpt-oss:20b", temperature=temperature)

# Initialize global LLM instance
llm = get_llm()

# Helper to ensure we always get the content string
def get_response_content(response):
    if hasattr(response, 'content'):
        return response.content
    return str(response)
