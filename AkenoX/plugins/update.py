import os
import asyncio
import subprocess
from pyrogram import Client, filters
from AkenoX import *

@RENDYDEV.user(prefix=["update"], filters=filters.me)
async def update_and_restart(client, message):
    status_message = await message.reply_text("🔄 Updating the bot...")

    try:
        # Pull latest changes from GitHub
        process = subprocess.run(["git", "pull"], capture_output=True, text=True)
        git_output = process.stdout + process.stderr

        if "Already up to date." in git_output:
            await status_message.edit("✅ Already up to date!")
            return
        
        # Rebuild the Docker container
        await status_message.edit("🔄 Rebuilding Docker container...")
        subprocess.run(["sudo", "docker", "build", "-t", "akenox-inline", "."], check=True)

        # Get running container ID
        container_id = subprocess.run(
            ["sudo", "docker", "ps", "-q", "-f", "ancestor=akenox-inline"],
            capture_output=True, text=True
        ).stdout.strip()

        if not container_id:
            await status_message.edit("⚠️ Error: No running container found!")
            return

        # Restart the container
        await status_message.edit("🚀 Restarting the bot...")
        subprocess.run(["sudo", "docker", "restart", container_id], check=True)

        await asyncio.sleep(2)
        await status_message.edit("✅ Update complete! Restarting...")

    except Exception as e:
        await status_message.edit(f"❌ Update failed:\n```\n{str(e)}\n```")

    finally:
        # Forcefully exit the process (Docker will restart it)
        os._exit(0)
