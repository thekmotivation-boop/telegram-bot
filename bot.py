import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNELS = [
    "@fxmepy",
    "@zorofxme"
]

FILE_PATH = "zfxme.py"


async def is_user_joined(context, user_id):
    try:
        for channel in CHANNELS:
            member = await context.bot.get_chat_member(channel, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        return True
    except:
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if await is_user_joined(context, user_id):
        await send_file(update.message)
    else:
        await send_join_message(update.message)


async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if await is_user_joined(context, user_id):
        await query.message.delete()
        await send_file(query.message)
    else:
        await query.answer("⚠️ Please join all channels first!", show_alert=True)


async def send_file(message):
    try:
        with open(FILE_PATH, "rb") as f:
            await message.reply_document(f)
    except:
        await message.reply_text("❌ File not found.")


async def send_join_message(message):
    keyboard = [
        [InlineKeyboardButton("Join Channel 1", url="https://t.me/fxmepy")],
        [InlineKeyboardButton("Join Channel 2", url="https://t.me/zorofxme")],
        [InlineKeyboardButton("TRY AGAIN", callback_data="check")]
    ]

    await message.reply_text(
        "Join all channels then click TRY AGAIN",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_join, pattern="check"))

print("🚀 Bot Running...")
app.run_polling()
