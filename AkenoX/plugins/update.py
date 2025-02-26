import os
import subprocess
import sys
import asyncio
from pyrogram import filters

from AkenoX import *


@RENDYDEV.user(prefix=["update"], filters=filters.me)
async def update_and_restart(client, message):
    await message.reply_text("🔄 Updating bot... Please wait!")

    try:
        # Pull latest changes from GitHub
        subprocess.run(["git", "pull"], check=True)

        # Stop the bot (Optional delay for safety)
        await message.reply_text("🛑 Stopping bot...")
        await asyncio.sleep(2)

        # Rebuild Docker image
        await message.reply_text("⚙️ Rebuilding Docker image...")
        subprocess.run(["sudo", "docker", "build", "-t", "akenox-inline", "."], check=True)

        # Restart bot
        await message.reply_text("🚀 Restarting bot...")
        subprocess.run(["sudo", "docker", "run", "-it", "--rm", "akenox-inline"], check=True)

    except subprocess.CalledProcessError as e:
        await message.reply_text(f"❌ Update failed!\nError: {str(e)}")
