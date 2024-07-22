import discord
from discord.ext import commands

from music_bot.config import *


class AdminCog(commands.Cog):
    """Cog for administrative commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setprefix")
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, prefix: str):
        """Sets the command prefix for the bot.

        Parameters:
            ctx (discord.ext.commands.Context): The context of the command.
            prefix (str): The new command prefix.
        """
        if len(prefix) > 1:
            await ctx.send("Prefix must be a single character.")
            return

        # Update the command prefix in the .env file (for simplicity)
        os.environ["COMMAND_PREFIX"] = prefix
        await ctx.send(f"Command prefix set to `{prefix}`.")

    @commands.command(name="setsource")
    @commands.has_permissions(administrator=True)
    async def set_source(self, ctx, source: str):
        """Sets the default music source for the bot.

        Parameters:
            ctx (discord.ext.commands.Context): The context of the command.
            source (str): The new default music source (youtube, spotify, soundcloud).
        """
        source = source.lower()
        if source not in ["youtube", "spotify", "soundcloud"]:
            await ctx.send("Invalid music source. Choose from: youtube, spotify, soundcloud.")
            return

        # Update the default music source in the .env file (for simplicity)
        os.environ["DEFAULT_MUSIC_SOURCE"] = source
        await ctx.send(f"Default music source set to `{source}`.")

    @commands.command(name="reload")
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx):
        """Reloads the bot's cogs.

        Parameters:
            ctx (discord.ext.commands.Context): The context of the command.
        """
        for cog in self.bot.cogs:
            self.bot.reload_extension(f"music_bot.cogs.{cog}")
        await ctx.send("Cogs reloaded.")