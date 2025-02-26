import os
import asyncio
import subprocess
from pyrogram import Client, filters
from AkenoX import *

@RENDYDEV.user(prefix=["update"], filters=filters.me)
async def update_and_restart(client, message):
    status_message = await message.reply_text("🔄 Updating the bot...")

    try:
        # Step 1: Pull latest changes from GitHub
        process = subprocess.run(["git", "pull"], capture_output=True, text=True)
        git_output = process.stdout + process.stderr

        if "Already up to date." in git_output:
            await status_message.edit("✅ Already up to date!")
            return
        
        # Step 2: Stop and remove the running container
        await status_message.edit("🛑 Stopping and removing old container...")
        subprocess.run(["sudo","docker", "stop", "akenox-inline"], check=False)
        subprocess.run(["sudo","docker", "rm", "akenox-inline"], check=False)
        await asyncio.sleep(2)

        # Step 3: Rebuild the Docker container
        await status_message.edit("🐳 Rebuilding Docker container...")
        subprocess.run(["sudo","docker", "build", "-t", "akenox-inline", "."], check=True)

        # Step 4: Restart the bot
        await status_message.edit("🚀 Restarting the bot...")
        subprocess.run(["sudo","docker", "run", "-d", "--restart", "always", "--name", "akenox-inline", "akenox-inline"], check=True)

        await asyncio.sleep(2)
        await status_message.edit("✅ Update complete! Restarting...")

    except subprocess.CalledProcessError as e:
        await status_message.edit(f"❌ Update failed:\n```\n{e.stderr}\n```")

    finally:
        # Forcefully exit the process (Docker will restart it)
        os._exit(0)
