from telegram import Update
from telegram.ext import ContextTypes

async def pdf_import(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📁 Please upload your PDF file for MCQ extraction.")

async def txt_import(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📄 Send your text file in standard formatted text.")

async def html_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💼 Generating HTML score card report...")
    
