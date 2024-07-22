import discord
from discord.ext import commands

class CommandError(Exception):
    """Base class for custom command errors."""
    pass

class MissingPermissionsError(CommandError):
    """Raised when a user lacks the required permissions to execute a command."""
    def __init__(self, missing_permissions):
        super().__init__()
        self.missing_permissions = missing_permissions

    def __str__(self):
        return f"You are missing the following permissions: {', '.join(self.missing_permissions)}"

class NoVoiceChannelError(CommandError):
    """Raised when the user is not in a voice channel."""
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "You are not connected to a voice channel."

class BotNotInVoiceChannelError(CommandError):
    """Raised when the bot is not in a voice channel."""
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "The bot is not currently in a voice channel."

class QueueIsEmptyError(CommandError):
    """Raised when the music queue is empty."""
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "The music queue is empty."

class SongNotFoundError(CommandError):
    """Raised when the requested song is not found."""
    def __init__(self, query):
        super().__init__()
        self.query = query

    def __str__(self):
        return f"Song not found: {self.query}"

class InvalidSongURL(CommandError):
    """Raised when the provided song URL is invalid."""
    def __init__(self, url):
        super().__init__()
        self.url = url

    def __str__(self):
        return f"Invalid song URL: {self.url}"