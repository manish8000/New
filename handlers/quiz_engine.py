from telegram import Update
from telegram.ext import ContextTypes

async def create_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛠️ Send your quiz title and questions to start building.")

async def launch_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Launching Quiz engine...")

async def stop_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛑 Quiz stopped immediately.")

async def speed_control(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.message.text.split()[0].replace('/', '')
    await update.message.reply_text(f"⚡ Quiz speed updated to: {cmd}")
    
