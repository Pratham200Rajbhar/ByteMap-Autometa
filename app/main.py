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

from fastapi import FastAPI
from contextlib import asynccontextmanager

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

I'm your intelligent assistant with **FULL CRUD** capabilities for managing the ByteMap website.

📝 **Blogs** - Create, list, update, delete
🗂️ **Projects** - Create, list, update, delete
🛠️ **Services** - Create, list, update, delete
⭐ **Testimonials** - Full management
❓ **FAQs** - Full management
📊 **Stats** - Full management
🏆 **Milestones** - Full management
💬 **Comments** - Create, list, delete
📬 **Contacts** - List, update, delete

**Quick Examples:**
• "Create blog about OSI model"
• "List all blogs"
• "Delete blog [slug]"
• "List all testimonials"

Type /help for more examples or /clear to reset conversation."""

    await update.message.reply_text(welcome_message, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_message = """🔧 **ByteMap Bot Help**

**Commands:**
• /start - Show welcome message
• /help - Show this help message
• /clear - Clear conversation history
• /status - Check bot status

**📝 Blog Examples:**
• "Create blog about [topic]"
• "Write blog on AI trends"
• "List all blogs"
• "Update blog [slug]"
• "Delete blog [slug]"

**🗂️ Project Examples:**
• "Create project [details]"
• "List all projects"
• "Update project [slug]"
• "Delete project [slug]"

**Other Resources:**
• "List all testimonials / FAQs / stats / milestones"
• "Create new testimonial / FAQ / stat / milestone"
• "List contact inquiries"
• "List all comments"

**Tips:**
• Be specific about what you want
• Use /clear if I seem confused
• I'll generate content automatically for blogs"""

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting ByteMap Automation Bot...")
    
    telegram_app = ApplicationBuilder().token(TOKEN).build()
    
    telegram_app.add_handler(CommandHandler("start", start_command))
    telegram_app.add_handler(CommandHandler("help", help_command))
    telegram_app.add_handler(CommandHandler("clear", clear_command))
    telegram_app.add_handler(CommandHandler("status", status_command))
    
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    await telegram_app.initialize()
    await telegram_app.start()
    
    if telegram_app.updater:
        await telegram_app.updater.start_polling(drop_pending_updates=True)
    
    print("✅ Bot is running! Listening for messages...")
    
    try:
        bot = Bot(token=TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text="🟢 ByteMap Bot is now online and ready!")
    except Exception as e:
        print(f"⚠️ Could not send startup message: {e}")
        
    yield
    
    print("🛑 Stopping ByteMap Automation Bot...")
    if telegram_app.updater:
        await telegram_app.updater.stop()
    await telegram_app.stop()
    await telegram_app.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def health_check():
    return {"status": "ok", "message": "ByteMap Automation Bot is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}


def main():
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)


if __name__ == "__main__":
    main()
