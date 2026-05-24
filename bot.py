import os
import requests

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🎬 Send YouTube link"
    )


async def get_video(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text.strip()

    msg = await update.message.reply_text(
        "📥 Processing..."
    )

    try:

        response = requests.post(
            "https://api.cobalt.tools/api/json",
            json={
                "url": url
            }
        )

        data = response.json()

        if "url" not in data:

            await msg.edit_text(
                "❌ Failed to fetch video."
            )

            return

        download_url = data["url"]

        await msg.edit_text(
            f"✅ Download Link:\n\n{download_url}"
        )

    except Exception as e:

        await msg.edit_text(
            f"❌ Error:\n{str(e)}"
        )


def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            get_video
        )
    )

    print("Bot running...")

    app.run_polling()


if __name__ == "__main__":
    main()
