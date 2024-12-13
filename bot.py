import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

assert TOKEN, "No DISCORD_TOKEN found in .env file"

# Define intents and bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Map each letter to the regional indicator emoji
def text_to_emoji_reactions(word):
    emoji_list = []
    for char in word.upper():
        if "A" <= char <= "Z":
            emoji_list.append(f"🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿"[ord(char) - ord("A")])
    return emoji_list

# Define the slash command
@bot.tree.command(name="reactemoji", description="React to a user's last message with emoji letters.")
async def reactemoji(interaction: discord.Interaction, username: str, word: str):
    if not interaction.guild:
        await interaction.response.send_message("This command can only be used in a server.")
        return

    # Find the user by nickname or username
    target_user = next(
        (m for m in interaction.guild.members if m.display_name == username or m.name == username), 
        None
    )
    
    if not target_user:
        await interaction.response.send_message(f"User '{username}' not found.")
        return

    # Search for the user's most recent message in the current channel
    target_message = None
    async for message in interaction.channel.history(limit=100):
        if message.author == target_user:
            target_message = message
            break

    if target_message:
        # Get the list of emojis corresponding to the word
        emoji_reactions = text_to_emoji_reactions(word)

        # React to the message with each emoji in sequence
        for emoji in emoji_reactions:
            await target_message.add_reaction(emoji)

        await interaction.response.send_message(f"Reacted to {username}'s message with emojis!")
    else:
        await interaction.response.send_message(f"Could not find a recent message from '{username}' in this channel.")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    # Sync commands with Discord
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s) to the server.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# Run the bot
bot.run(TOKEN)
