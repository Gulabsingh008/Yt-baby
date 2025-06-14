# bot/plugins/pinterest.py

import os
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("pinterest") & filters.private)
async def pinterest_handler(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("❌ Please provide a Pinterest URL!\n\nUsage: `/pinterest <url>`", quote=True)

    pinterest_url = message.command[1]
    await message.reply("🔍 Downloading... Please wait", quote=True)

    try:
        cookies_path = os.path.abspath("cookies.txt")
        output_path = os.path.abspath("pinterest.%(ext)s")

        command = [
            "yt-dlp",
            "--cookies", cookies_path,
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "--add-header", "Accept-Language: en-US,en;q=0.9",
            "--add-header", "Referer: https://www.pinterest.com/",
            "-o", output_path,
            pinterest_url
        ]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            # Find downloaded file
            for ext in ["mp4", "webm", "mkv", "jpg", "png"]:
                file_path = f"pinterest.{ext}"
                if os.path.exists(file_path):
                    await message.reply_document(file_path, caption="✅ Here is your downloaded file.")
                    os.remove(file_path)
                    return
            await message.reply("❌ Download completed but file not found.")
        else:
            await message.reply(f"❌ Download failed:\n\n`{result.stderr}`")
    except Exception as e:
        await message.reply(f"❌ Error occurred: `{str(e)}`")
