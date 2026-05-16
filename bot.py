import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")

users = {}

keyboard = [
    ["📋 Tasks", "💰 Balance"],
    ["👥 Invite", "💳 Withdraw"]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in users:
        users[user_id] = {"points": 0, "referrals": 0}

    await update.message.reply_text(
        "🚀 Welcome to Earnify!\nEarn airtime & data by completing simple tasks.",
        reply_markup=reply_markup
    )

async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 Task:\nJoin https://t.me/example\nReward: 20 points\nType /done after joining"
    )

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users[user_id]["points"] += 20

    await update.message.reply_text(
        f"✅ Done! Balance: {users[user_id]['points']} points"
    )

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    points = users.get(user_id, {}).get("points", 0)

    await update.message.reply_text(f"💰 Balance: {points} points")

async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    link = f"https://t.me/YOUR_BOT_USERNAME?start={user_id}"

    await update.message.reply_text(f"👥 Invite:\n{link}")

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💳 Withdrawal request sent!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📋 Tasks":
        await tasks(update, context)
    elif text == "💰 Balance":
        await balance(update, context)
    elif text == "👥 Invite":
        await referral(update, context)
    elif text == "💳 Withdraw":
        await withdraw(update, context)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tasks", tasks))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("referral", referral))
    app.add_handler(CommandHandler("withdraw", withdraw))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
