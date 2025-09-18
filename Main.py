import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from pytube import YouTube
import instaloader

# حط التوكن تبعك هون
TOKEN = "7952293262:AAHiOP-5oy5RABrjqOVlQVnHP_NHTnrgPr0"

# إنستا لودر
L = instaloader.Instaloader(dirname_pattern="downloads", download_videos=True, save_metadata=False)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 هلا! ابعتلي رابط يوتيوب أو إنستغرام ريلز 🔥")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    try:
        if "youtube.com" in url or "youtu.be" in url:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            file_path = stream.download(filename="ytvideo.mp4")

            await update.message.reply_video(video=open(file_path, "rb"))
            os.remove(file_path)

        elif "instagram.com/reel" in url:
            # رح ينزل الفيديو داخل مجلد downloads
            L.download_post(instaloader.Post.from_shortcode(L.context, url.split("/")[-2]), target="downloads")
            # جيب أول فيديو من مجلد downloads
            for file in os.listdir("downloads"):
                if file.endswith(".mp4"):
                    await update.message.reply_video(video=open(f"downloads/{file}", "rb"))
                    os.remove(f"downloads/{file}")

        else:
            await update.message.reply_text("❌ الرابط مو مدعوم. جرب يوتيوب أو إنستا ريلز.")

    except Exception as e:
        await update.message.reply_text(f"⚠️ صار خطأ: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    app.run_polling()

if __name__ == "__main__":
    main()
