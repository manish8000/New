import logging
import json
import sqlite3
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import TELEGRAM_TOKEN, OWNER_ID
from database import init_db
from handlers.ai_groq import generate_ai_quiz

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Database Initialization
init_db()

# --- BASIC COMMAND HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🪐 Bot is Alive and running fine!")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = "🧭 **Available Commands:**\n/start, /quiz, /stats, /create, /aiquiz, /pdfimport, /txtimport, /broadcast, /premium, etc."
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect("quiz_bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT quizzes_taken, correct_answers, wrong_answers FROM stats WHERE user_id=?", (update.effective_user.id,))
    data = cursor.fetchone()
    conn.close()
    
    if data:
        await update.message.reply_text(f"📊 **Your Stats:**\n\nQuizzes: {data[0]}\nCorrect: {data[1]}\nWrong: {data[2]}")
    else:
        await update.message.reply_text("📊 No stats found yet. Start playing quizzes!")

async def userprofile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"👨‍💼 **User Profile:**\nName: {user.full_name}\nID: `{user.id}`", parse_mode="Markdown")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👤 **Quiz Creator Info:**\nBuilt with Python-Telegram-Bot, Groq AI & SQLite.")

async def features(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎟️ **Features:**\n- AI Auto Quiz Generation\n- PDF/TXT Import\n- Negative Marking\n- Speed Control\n- HTML Reports")

async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💎 **Premium:** Upgrade to access unlimited AI generations and bulk PDF conversions!")

# --- AI COMMAND HANDLER ---
async def aiquiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args) if context.args else "General Knowledge"
    await update.message.reply_text(f"🤖 Generating AI Quiz on *{topic}* using Groq API...", parse_mode="Markdown")
    
    result = await generate_ai_quiz(topic)
    if result:
        await update.message.reply_text(f"```json\n{result[:3500]}\n```", parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Groq API key is missing or failed to generate quiz.")

# --- DUMMY PLACEHOLDERS FOR REMAINING REQUESTED COMMANDS ---
COMMAND_LIST = [
    "quiz", "add", "edit", "delete", "poll2q", "scrapepoll", "clone", "queue",
    "pdfimport", "txtimport", "quizid", "pdfinfo", "htmlinfo", "htmlreport",
    "negmark", "resetpenalty", "stop", "cancel", "create", "myquizzes",
    "delquizdb", "pause", "resume", "fast", "slow", "normal", "broadcast",
    "stopcast", "ban", "unban", "mocktest", "users", "chats", "banlist",
    "leavegrp", "schedule", "html", "tx2html", "pdf2txt", "pdf2mcq", "auth",
    "rem_auth", "mute", "unmute"
]

async def generic_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.message.text.split()[0].replace('/', '')
    await update.message.reply_text(f"⚙️ Command `/{cmd}` triggered. Ready for custom logic.", parse_mode="Markdown")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Specific Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("userprofile", userprofile))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("features", features))
    app.add_handler(CommandHandler("premium", premium))
    app.add_handler(CommandHandler("aiquiz", aiquiz))
    
    # Generic Handler Registration for all other requested commands
    for cmd in COMMAND_LIST:
        app.add_handler(CommandHandler(cmd, generic_handler))
        
    print("🤖 Quiz Bot Started Successfully!")
    app.run_polling()

if __name__ == "__main__":
    main()

