import sys
import os

# Allow imports from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage

from agent.tools import ALL_TOOLS


# =========================
# System Prompt
# =========================
SYSTEM_PROMPT = """You are ByteMap's intelligent automation assistant. You help manage the ByteMap website through Telegram commands.

You have access to tools for:
- 📝 Blog Management: Create, list, and view blog posts
- 🗂️ Project Management: Create, list, and view portfolio projects
- 🛠️ Services: View available services
- 📬 Contact Inquiries: View customer contact submissions
- 💬 Comments: View and add blog comments
- ✨ Content Generation: Generate professional content using AI

Guidelines:
1. When asked to write/create a blog, use the create_blog_post tool with an appropriate topic
2. When asked to list items, use the corresponding list tool
3. Always provide helpful, formatted responses
4. If you're unsure what the user wants, ask for clarification
5. Be concise but informative in your responses

Response Format:
- Use emojis to make responses visually appealing
- Format lists clearly
- Confirm successful actions
- Report errors clearly with suggestions

You are interacting through Telegram, so keep responses mobile-friendly and easy to read.
"""


# =========================
# Agent Factory
# =========================
def create_agent():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
    )

    agent = create_react_agent(
        model=llm,
        tools=ALL_TOOLS,
        prompt=SYSTEM_PROMPT
    )

    return agent


# =========================
# Agent Wrapper Class
# =========================
class ByteMapAgent:
    def __init__(self):
        self.agent = create_agent()
        self.chat_history: list = []

    async def process_message(self, message: str) -> str:
        try:
            # Build conversation state
            messages = self.chat_history + [
                HumanMessage(content=message)
            ]

            # ✅ async-safe invocation
            result = await self.agent.ainvoke({
                "messages": messages
            })

            ai_messages = result.get("messages", [])
            response_text = None

            # Get last AI response
            for msg in reversed(ai_messages):
                if isinstance(msg, AIMessage) and msg.content:
                    response_text = msg.content
                    break

            if not response_text:
                response_text = "🤖 I couldn’t process that request. Please try again."

            # Store conversation history
            self.chat_history.extend([
                HumanMessage(content=message),
                AIMessage(content=response_text)
            ])

            # Keep only last 20 messages
            self.chat_history = self.chat_history[-20:]

            return response_text

        except Exception as e:
            print(f"[ByteMapAgent ERROR]: {e}")
            return f"❌ An error occurred:\n{str(e)}"

    def clear_history(self) -> str:
        self.chat_history = []
        return "🔄 Conversation history cleared!"


# =========================
# Singleton Accessor
# =========================
bytemap_agent: ByteMapAgent | None = None


def get_agent() -> ByteMapAgent:
    global bytemap_agent
    if bytemap_agent is None:
        bytemap_agent = ByteMapAgent()
    return bytemap_agent
