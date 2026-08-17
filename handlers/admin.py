import sqlite3
from telegram import Update
from telegram.ext import ContextTypes
from config import OWNER_ID

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("⛔ Admin access required.")
        return
    msg = " ".join(context.args)
    if not msg:
        await update.message.reply_text("⚠️ Usage: /broadcast [Your message]")
        return
    await update.message.reply_text(f"📢 Broadcasting: {msg}")

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    if context.args:
        user_id = context.args[0]
        conn = sqlite3.connect("quiz_bot.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_banned = 1 WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        await update.message.reply_text(f"🚫 User `{user_id}` banned successfully.", parse_mode="Markdown")

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    if context.args:
        user_id = context.args[0]
        conn = sqlite3.connect("quiz_bot.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_banned = 0 WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        await update.message.reply_text(f"♻️ User `{user_id}` unbanned successfully.", parse_mode="Markdown")

async def users_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    conn = sqlite3.connect("quiz_bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    await update.message.reply_text(f"👥 Total Registered Users: {count}")
    
