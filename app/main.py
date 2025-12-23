import os
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

async def receive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    print("Received Text:", text)

def main():
    bot = Bot(token=TOKEN)
    bot.send_message(chat_id=CHAT_ID, text="Hello")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive))

    print("Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
