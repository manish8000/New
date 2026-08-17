from groq import Groq
from telegram import Update
from telegram.ext import ContextTypes
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

async def aiquiz_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args) if context.args else "General Knowledge"
    await update.message.reply_text(f"🤖 Generating AI Quiz on *{topic}* using Groq API...", parse_mode="Markdown")
    
    if not client:
        await update.message.reply_text("❌ GROQ_API_KEY environment variable missing or empty.")
        return

    try:
        prompt = f"Generate a JSON list of 5 quiz questions on '{topic}'. Format: [{{\"question\": \"...\", \"options\": [\"A\", \"B\", \"C\", \"D\"], \"correct_index\": 0}}]"
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        res = completion.choices[0].message.content
        await update.message.reply_text(f"```json\n{res[:3500]}\n```", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"⚠️ AI Generation Failed: {str(e)}")
        
