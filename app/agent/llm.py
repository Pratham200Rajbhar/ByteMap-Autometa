import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

load_dotenv()


def get_llm(
    model: str = "gemini-2.5-flash",
    temperature: float = 0.7,
):
    return ChatGoogleGenerativeAI(
        model=model,
        temperature=temperature,
    )


def get_llm(
    model: str = "llama3.2",
    temperature: float = 0.7,
):
    return ChatOllama(
        model=model,
        temperature=temperature,
    )

llm = get_llm()

