import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_llm(
    model: str = "gemini-2.5-flash",
    temperature: float = 0.7,
):
    """
    Returns a Google Gemini LLM instance.
    
    Args:
        model: The Gemini model to use (default: gemini-2.5-flash)
        temperature: Controls randomness in responses (default: 0.7)
    
    Returns:
        ChatGoogleGenerativeAI instance
    """
    return ChatGoogleGenerativeAI(
        model=model,
        temperature=temperature,
    )


# Default LLM instance
llm = get_llm()
