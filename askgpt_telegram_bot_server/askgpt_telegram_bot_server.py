import logging
import os

import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

ASKGPT_SERVER = "http://localhost:8888"


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        if incoming_msg := update.effective_message:
            query = incoming_msg.text
            print(f"Query: {query}")
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                f"{ASKGPT_SERVER}/qa", json={"q": query}, headers=headers
            ).json()
            print(f"Response: {response}")
            await incoming_msg.reply_text(response["ChatGPT"])


def main():
    TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    if TELEGRAM_BOT_TOKEN is None:
        print("TELEGRAM_BOT_TOKEN not found")
        return
    telegram_bot = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    start_handler = CommandHandler("ask", ask)
    telegram_bot.add_handler(start_handler)
    telegram_bot.run_polling()
