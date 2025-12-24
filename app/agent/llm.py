import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def get_llm(temperature: float = 0.7):
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=temperature)

llm = get_llm()

