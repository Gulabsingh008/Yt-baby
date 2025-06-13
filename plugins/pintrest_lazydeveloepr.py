import subprocess
import os
import time
from pyrogram import enums

TMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./DOWNLOADS/")

def yt_dlp_download_pinterest(pinterest_url):
    try:
        if not os.path.exists(TMP_DOWNLOAD_DIRECTORY):
            os.makedirs(TMP_DOWNLOAD_DIRECTORY)

        command = [
            "yt-dlp",
            "--cookies", "cookies.txt",
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "--add-header", "Accept-Language: en-US,en;q=0.9",
            "--add-header", "Referer: https://www.pinterest.com/",
            "-o", f"{TMP_DOWNLOAD_DIRECTORY}%(title).80s.%(ext)s",
            pinterest_url
        ]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            for line in reversed(result.stdout.splitlines()):
                if "[download] Destination:" in line:
                    return line.split("Destination:")[1].strip()
        else:
            print("Error downloading:", result.stderr)
            return None
    except Exception as e:
        print("Download exception:", e)
        return None


async def download_pintrest_vid(client, message, url):
    try:
        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)

        ms = await message.reply("<i>📥 Downloading Pinterest video...</i>")
        file_path = yt_dlp_download_pinterest(url)

        if file_path and os.path.exists(file_path):
            await client.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_VIDEO)
            await ms.edit_text("⚡ Download complete! Sending video...")
            await message.reply_video(file_path)

            # Optional: Auto-delete after some time
            os.remove(file_path)
        else:
            await ms.edit_text("❌ Failed to download video. Please check the link or try again later.")
    except Exception as e:
        await message.reply(f"❌ Error occurred: {str(e)}")
