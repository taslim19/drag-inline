from urllib.parse import quote
import aiohttp
from pyrogram.enums import ChatAction, ParseMode
from AkenoX import *
from config import api_key

# Function to fetch Instagram reel video URL
async def fetch_instagram_reel(video_url):
    encoded_url = quote(video_url)  # Encode the URL properly
    api_url = f"https://randydev-ryu-js.hf.space/api/v1/dl/instagram-v4?url={encoded_url}"
    headers = {"x-api-key": api_key}

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                if data.get("results") and data["results"].get("results"):
                    return data["results"]["results"][0]["variants"][0]["url"]
            return None

# Command handler 
@RENDYDEV.user(prefix=["ig"], filters=(filters.me & ~filters.forwarded))
async def insta_download_command(client, message):
    chat_id = message.chat.id
    await message.reply_chat_action(ChatAction.UPLOAD_VIDEO)

    if len(message.command) < 2:
        await message.reply_text("Exᴀᴍᴘʟᴇ ᴜsᴀɢᴇ: ig [Instagram Reel URL]", parse_mode=ParseMode.HTML)
        return

    video_url = message.command[1]  # Extract the Instagram reel URL
    download_url = await fetch_instagram_reel(video_url)

    if download_url:
        await message.reply_video(video=download_url, caption="Here is your Instagram reel ")
    else:
        await message.reply_text("❌ Failed to fetch the Instagram reel. Please check the URL and try again.")

# Adding the command to the bot's button panel
RENDYDEV.buttons(
    "instagram", [
        ["ig [Instagram Reel URL]", "Download an Instagram reel video."],
    ],
)
