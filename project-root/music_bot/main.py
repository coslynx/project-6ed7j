import discord
from discord.ext import commands
import logging

import os
from dotenv import load_dotenv

from music_bot.config import *
from music_bot.cogs.music import MusicCog
from music_bot.cogs.admin import AdminCog

load_dotenv()

# Set up logging
logging.basicConfig(level=LOGGING_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

# Create Discord bot instance
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# Load cogs
bot.add_cog(MusicCog(bot))
bot.add_cog(AdminCog(bot))

# Set bot activity
bot.activity = discord.Activity(type=ACTIVITY_TYPE, name=ACTIVITY_NAME)

@bot.event
async def on_ready():
    """Event handler for when the bot is ready."""
    logging.info(f'Logged in as {bot.user.name} (ID: {bot.user.id})')

# Run the bot
if __name__ == '__main__':
    try:
        bot.run(DISCORD_TOKEN)
    except discord.errors.LoginFailure:
        logging.error('Invalid Discord token. Please check your .env file.')
    except Exception as e:
        logging.error(f'An error occurred while running the bot: {e}')