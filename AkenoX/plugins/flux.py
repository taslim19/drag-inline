from pyrogram import filters
from AkenoX import *  # Make sure this is correctly defined
import aiohttp
import io
from config import api_key

# Function to fetch raw image data from FLUX API
async def fetch_image_from_flux(question):
    url = "https://randydev-ryu-js.hf.space/api/v1/flux/black-forest-labs/flux-1-schnell"  # FLUX API endpoint
    headers = {"x-api-key": api_key}
    params = {"query": question}  # Pass query as a parameter
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                return await response.read()  # Return raw image data
            else:
                return None

# Command handler for flux
@RENDYDEV.user(prefix=["flux"], filters=(filters.me & ~filters.forwarded))
async def flux_command(client, message):
    if len(message.command) < 2:
        await message.reply_text("Exᴀᴍᴘʟᴇ ᴜsᴀɢᴇ: flux [your query]")
        return
    
    question = " ".join(message.command[1:])  # Extract the query
    image_data = await fetch_image_from_flux(question)
    
    if image_data:
        image_stream = io.BytesIO(image_data)
        image_stream.name = "flux_result.jpg"  # Set filename
        await message.reply_photo(photo=image_stream, caption="Here is your generated image")
    else:
        await message.reply_text("Failed to fetch image from FLUX API.")
