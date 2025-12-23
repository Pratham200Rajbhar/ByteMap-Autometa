import os
import sys
import asyncio

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

from agent.agent import get_agent


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name or "User"
    
    print(f"📨 Received from {user_name}: {user_message}")
    
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    
    try:
        agent = get_agent()
        response = await agent.process_message(user_message)
        
        if len(response) > 4000:
            chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk, parse_mode="Markdown")
        else:
            try:
                await update.message.reply_text(response, parse_mode="Markdown")
            except Exception:
                await update.message.reply_text(response)
        
        print(f"✅ Response sent to {user_name}")
        
    except Exception as e:
        error_msg = f"❌ Sorry, an error occurred: {str(e)}"
        print(f"❌ Error processing message: {e}")
        await update.message.reply_text(error_msg)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = """👋 **Welcome to ByteMap Automation Bot!**

I'm your intelligent assistant for managing the ByteMap website. Here's what I can do:

📝 **Blog Management**
• "Write a blog about [topic]"
• "List all blogs"
• "Show blog details for [slug]"

🗂️ **Project Management**
• "List all projects"
• "Create a project about [topic]"

🛠️ **Services & Inquiries**
• "Show all services"
• "List contact inquiries"
• "Show all comments"

Just send me a message describing what you want to do, and I'll take care of it!

Type /help for more information or /clear to reset our conversation."""

    await update.message.reply_text(welcome_message, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_message = """🔧 **ByteMap Bot Help**

**Commands:**
• /start - Show welcome message
• /help - Show this help message
• /clear - Clear conversation history
• /status - Check bot status

**Example Messages:**
• "Write a blog about environmental pollution"
• "List all the blogs we have"
• "Show me the latest contact inquiries"
• "Create a project for an e-commerce website"

**Tips:**
• Be specific about what you want
• I can generate content automatically
• I'll ask for clarification if needed

Need help? Just describe what you're trying to do!"""

    await update.message.reply_text(help_message, parse_mode="Markdown")


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    agent = get_agent()
    result = agent.clear_history()
    await update.message.reply_text(result)


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_message = """✅ **Bot Status: Online**

🤖 Agent: Active
🔗 API: Connected
💬 Ready to process commands

Send me a message to get started!"""
    
    await update.message.reply_text(status_message, parse_mode="Markdown")


def main():
    print("🚀 Starting ByteMap Automation Bot...")
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("clear", clear_command))
    app.add_handler(CommandHandler("status", status_command))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Bot is running! Listening for messages...")
    print(f"📱 Chat ID: {CHAT_ID}")
    
    try:
        bot = Bot(token=TOKEN)
        asyncio.run(
            bot.send_message(chat_id=CHAT_ID, text="🟢 ByteMap Bot is now online and ready!")
        )
    except Exception as e:
        print(f"⚠️ Could not send startup message: {e}")
    
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
