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
        
        # Step 2: Reinstall dependencies (if needed)
        await status_message.edit("📦 Updating dependencies...")
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

        # Step 3: Restart the bot (without stopping the container)
        await status_message.edit("🚀 Restarting the bot...")

        # Start the bot again inside the running container
        subprocess.Popen(["python3", "-m", "AkenoX"])

        await asyncio.sleep(2)
        await status_message.edit("✅ Update complete! Bot restarted!")

    except subprocess.CalledProcessError as e:
        await status_message.edit(f"❌ Update failed:\n```\n{e.stderr}\n```")
