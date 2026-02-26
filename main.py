import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8302026789:AAEQg99Qx4M4ot8Rk_SzAIGbc7CwrUFmUYQ"

# Base de datos simple en memoria (fase 1)
users = {}

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "xp": 0,
            "coins": 0,
            "level": 1,
            "booster": 1
        }
    return users[user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = get_user(user.id)

    keyboard = [
        [InlineKeyboardButton("⚡ TAP", callback_data="tap")]
    ]

    await update.message.reply_text(
        f"⚡ ZeusProtocol PRO ⚡\n\n"
        f"Level: {data['level']}\n"
        f"XP: {data['xp']}\n"
        f"Coins: {data['coins']}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def tap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    data = get_user(user_id)

    bonus = data["booster"] * 0.01

    data["xp"] += int(1 + bonus)
    data["coins"] += int(1 + bonus)

    if data["xp"] > data["level"] * 75:
        data["level"] += 1
        data["xp"] = 0

    await query.answer("⚡ Tap!")

    await query.edit_message_text(
        f"⚡ ZeusProtocol PRO ⚡\n\n"
        f"Level: {data['level']}\n"
        f"XP: {data['xp']}\n"
        f"Coins: {data['coins']}"
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(tap, pattern="tap"))

    app.run_polling()

if __name__ == "__main__":
    main()
