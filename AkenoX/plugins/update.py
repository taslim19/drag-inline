import os
import subprocess
import sys

from pyrogram import filters

from AkenoX import *


@RENDYDEV.user(prefix=["update"], filters=filters.me)
async def update_and_restart(client, message):
    await message.reply_text("🔄 Updating bot... Please wait!")

    try:
        # Pull latest changes from GitHub
        subprocess.run(["git", "pull"], check=True)

        # Stop the current container (Assuming the bot is running inside Docker)
        await message.reply_text("🛑 Stopping bot...")
        await asyncio.sleep(2)

        # Rebuild and restart the container
        await message.reply_text("⚙️ Rebuilding Docker image...")
        subprocess.run(["sudo", "docker", "build", "-t", "akenox-inline", "."], check=True)

        await message.reply_text("🚀 Restarting bot...")
        subprocess.run(["sudo", "docker", "run", "-it", "--rm", "akenox-inline"], check=True)

    except subprocess.CalledProcessError as e:
        await message.reply_text(f"❌ Update failed!\nError: {str(e)}")
