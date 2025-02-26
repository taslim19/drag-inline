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
            await status_message.edit(" Already up to date!")
            return
        
        # Rebuild the Docker container (Runs on the HOST machine, not inside the container)
        await status_message.edit(" Rebuilding Docker container...")
        subprocess.run(["sudo", "docker", "build", "-t", "akenox-inline", "."], check=True)

        # Get container name from environment variable
        container_name = os.getenv("CONTAINER_NAME")
        if not container_name:
            await status_message.edit("Error: CONTAINER_NAME environment variable is not set.")
            return

        # Restart the container
        await status_message.edit("Restarting the bot...")
        subprocess.run(["sudo", "docker", "restart", container_name], check=True)

        # Delay before exit
        await asyncio.sleep(2)
        
    except Exception as e:
        await status_message.edit(f"❌ Update failed:\n```\n{str(e)}\n```")

    finally:
        # Stop the bot process so Docker restarts it
        await client.stop()
