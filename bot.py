import os

from pytubefix import YouTube

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


async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text.strip()

    msg = await update.message.reply_text(
        "📥 Downloading..."
    )

    try:

        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        yt = YouTube(url)

        stream = yt.streams.get_highest_resolution()

        file_path = stream.download(
            output_path="downloads"
        )

        await msg.edit_text(
            "📤 Uploading..."
        )

        with open(file_path, "rb") as video:

            await update.message.reply_video(
                video=video,
                supports_streaming=True
            )

        os.remove(file_path)

        await msg.edit_text(
            "✅ Done!"
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
            download_video
        )
    )

    print("Bot running...")

    app.run_polling()


if __name__ == "__main__":
    main()
