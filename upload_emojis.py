import discord
import os
from discord.ext import commands

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

assert TOKEN, "No DISCORD_TOKEN found in .env file"
assert GUILD, "No DISCORD_GUILD found in .env file"

GUILD = int(GUILD)

# Specify the directory where your emoji files are stored
EMOJI_DIR = './emojis'  # Make sure to update this path with your emoji files location

intents = discord.Intents.default()
intents.messages = True

# Set up the bot
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    
    # Make sure you're in a guild
    guild = bot.get_guild(GUILD)  # Replace with your server's guild ID
    if guild:
        # Iterate over each emoji image file in the directory
        for filename in os.listdir(EMOJI_DIR):
            if filename.endswith(('.png', '.jpg', '.gif')):
                emoji_name = filename.split('.')[0]  # Remove the file extension
                emoji_path = os.path.join(EMOJI_DIR, filename)

                # Open the image file and create the custom emoji
                with open(emoji_path, 'rb') as emoji_file:
                    await guild.create_custom_emoji(
                        name=emoji_name,
                        image=emoji_file.read()
                    )
                print(f"Uploaded emoji: {emoji_name}")
    else:
        print("Could not find the specified guild.")

# Run the bot
bot.run(TOKEN)
