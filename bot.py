import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8524619804:AAEbyx32pUDdQeMf-lepQTeJxs3joQ6kD5U"

CHANNELS = [
    "@fxmepy",
    "@zorofxme"
]

FILE_PATH = "zfxme.py"

# ================= JOIN CHECK FUNCTION ================= #

async def is_user_joined(context, user_id):
    try:
        for channel in CHANNELS:
            member = await context.bot.get_chat_member(channel, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        return True
    except:
        return False

# ================= START COMMAND ================= #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if await is_user_joined(context, user_id):
        await send_file(update.message)
    else:
        await send_join_message(update.message)

# ================= BUTTON CHECK ================= #

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if await is_user_joined(context, user_id):
        await query.message.delete()
        await send_file(query.message)
    else:
        await query.answer("⚠️ Please join all channels first!", show_alert=True)

# ================= SEND FILE ================= #

async def send_file(message):
    if not os.path.exists(FILE_PATH):
        await message.reply_text("❌ File not found.")
        return

    with open(FILE_PATH, "rb") as f:
        await message.reply_document(
            document=f,
            filename="zfxme.py",
            caption="🔥 Here is your file — zfxme.py"
        )

# ================= SEND JOIN MESSAGE ================= #

async def send_join_message(message):
    text = """
✨ 𝗛𝗲𝘆.. 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗙𝗫𝗠𝗘 𝗔𝗥𝗠𝗬 ✨

📢 Join all channels to get the file.

After joining, click "TRY AGAIN" below.
"""

    keyboard = [
        [InlineKeyboardButton("🔹 Join Channel 1", url="https://t.me/fxmepy")],
        [InlineKeyboardButton("🔹 Join Channel 2", url="https://t.me/zorofxme")],
        [InlineKeyboardButton("✅ TRY AGAIN", callback_data="check_join")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await message.reply_text(text, reply_markup=reply_markup)

# ================= MAIN ================= #

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))

print("🚀 Bot Running...")
app.run_polling()
