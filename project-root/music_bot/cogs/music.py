import discord
from discord.ext import commands
import asyncio
import youtube_dl
import requests
from spotipy import Spotify
from soundcloud import Client as SoundCloudClient
import pyaudio
from pydub import AudioSegment
import ffmpeg

from music_bot.utils.music import MusicPlayer

# Suppress noisy YouTube DL logging
youtube_dl.utils.bug_reports_message = lambda: ''

class MusicCog(commands.Cog):
    """Cog for music-related commands."""

    def __init__(self, bot):
        self.bot = bot
        self.music_player = MusicPlayer()
        self.voice_client = None

    @commands.command(name='play')
    async def play(self, ctx, *, query: str):
        """Plays a song from YouTube, Spotify, or SoundCloud.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            query (str): The search query or URL of the song.
        """
        try:
            # Check if the user is in a voice channel
            if not ctx.author.voice:
                await ctx.send("You are not connected to a voice channel.")
                return

            # Check if the bot is already in a voice channel
            if not self.voice_client:
                # Connect the bot to the user's voice channel
                self.voice_client = await ctx.author.voice.channel.connect()
            elif self.voice_client.channel != ctx.author.voice.channel:
                await self.voice_client.move_to(ctx.author.voice.channel)

            # Determine the music source
            source = query.lower()
            if 'youtube' in source:
                await self.play_youtube(ctx, query)
            elif 'spotify' in source:
                await self.play_spotify(ctx, query)
            elif 'soundcloud' in source:
                await self.play_soundcloud(ctx, query)
            else:
                await self.play_youtube(ctx, query)  # Default to YouTube

        except Exception as e:
            await ctx.send(f"An error occurred while playing the song: {e}")

    async def play_youtube(self, ctx, query):
        """Plays a song from YouTube."""
        try:
            # Download and stream the YouTube video
            with youtube_dl.YoutubeDL({'format': 'bestaudio'}) as ydl:
                info = ydl.extract_info(query, download=False)
                url = info['formats'][0]['url']
                title = info['title']
                artist = info['uploader']

            # Add the song to the queue and start playback
            await self.music_player.add_to_queue(ctx, url, title, artist)
            await self.music_player.play(self.voice_client)
            await ctx.send(f"Now playing: {title} by {artist}")

        except Exception as e:
            await ctx.send(f"An error occurred while playing the YouTube song: {e}")

    async def play_spotify(self, ctx, query):
        """Plays a song from Spotify."""
        try:
            # Get the Spotify API credentials from the .env file
            spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
            spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

            # Create a Spotify client
            spotify = Spotify(client_id=spotify_client_id, client_secret=spotify_client_secret)

            # Get the track ID from the query (assume a track URL for now)
            track_id = query.split('/')[-1]

            # Get the track information
            track_info = spotify.track(track_id)

            # Get the track URL (for streaming)
            track_url = track_info['external_urls']['spotify']

            # Add the song to the queue and start playback
            await self.music_player.add_to_queue(ctx, track_url, track_info['name'], track_info['artists'][0]['name'])
            await self.music_player.play(self.voice_client)
            await ctx.send(f"Now playing: {track_info['name']} by {track_info['artists'][0]['name']}")

        except Exception as e:
            await ctx.send(f"An error occurred while playing the Spotify song: {e}")

    async def play_soundcloud(self, ctx, query):
        """Plays a song from SoundCloud."""
        try:
            # Get the SoundCloud API credentials from the .env file
            soundcloud_client_id = os.getenv('SOUNDCLOUD_CLIENT_ID')
            soundcloud_client_secret = os.getenv('SOUNDCLOUD_CLIENT_SECRET')

            # Create a SoundCloud client
            soundcloud = SoundCloudClient(client_id=soundcloud_client_id, client_secret=soundcloud_client_secret)

            # Get the track ID from the query (assume a track URL for now)
            track_id = query.split('/')[-1]

            # Get the track information
            track_info = soundcloud.get('/tracks/' + track_id)

            # Get the track URL (for streaming)
            track_url = track_info['stream_url']

            # Add the song to the queue and start playback
            await self.music_player.add_to_queue(ctx, track_url, track_info['title'], track_info['user']['username'])
            await self.music_player.play(self.voice_client)
            await ctx.send(f"Now playing: {track_info['title']} by {track_info['user']['username']}")

        except Exception as e:
            await ctx.send(f"An error occurred while playing the SoundCloud song: {e}")

    @commands.command(name='skip')
    async def skip(self, ctx):
        """Skips the current song in the queue."""
        try:
            if not self.voice_client:
                await ctx.send("The bot is not currently playing music.")
                return

            # Skip the current song
            await self.music_player.skip(self.voice_client)
            await ctx.send("Skipping to the next song.")

        except Exception as e:
            await ctx.send(f"An error occurred while skipping the song: {e}")

    @commands.command(name='stop')
    async def stop(self, ctx):
        """Stops the current playback and clears the queue."""
        try:
            if not self.voice_client:
                await ctx.send("The bot is not currently playing music.")
                return

            # Stop the music and clear the queue
            await self.music_player.stop(self.voice_client)
            await ctx.send("Stopped the music and cleared the queue.")

            # Disconnect the bot from the voice channel
            await self.voice_client.disconnect()
            self.voice_client = None

        except Exception as e:
            await ctx.send(f"An error occurred while stopping the music: {e}")

    @commands.command(name='pause')
    async def pause(self, ctx):
        """Pauses the current playback."""
        try:
            if not self.voice_client:
                await ctx.send("The bot is not currently playing music.")
                return

            # Pause the music
            await self.music_player.pause(self.voice_client)
            await ctx.send("Paused the music.")

        except Exception as e:
            await ctx.send(f"An error occurred while pausing the music: {e}")

    @commands.command(name='resume')
    async def resume(self, ctx):
        """Resumes the paused playback."""
        try:
            if not self.voice_client:
                await ctx.send("The bot is not currently playing music.")
                return

            # Resume the music
            await self.music_player.resume(self.voice_client)
            await ctx.send("Resumed the music.")

        except Exception as e:
            await ctx.send(f"An error occurred while resuming the music: {e}")

    @commands.command(name='queue')
    async def queue(self, ctx):
        """Displays the current music queue."""
        try:
            if not self.music_player.queue:
                await ctx.send("The queue is empty.")
                return

            # Build the queue message
            queue_message = "**Queue:**\n"
            for i, song in enumerate(self.music_player.queue):
                queue_message += f"{i+1}. {song['title']} by {song['artist']}\n"

            await ctx.send(queue_message)

        except Exception as e:
            await ctx.send(f"An error occurred while displaying the queue: {e}")

    @commands.command(name='volume')
    async def volume(self, ctx, volume: int):
        """Adjusts the playback volume.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            volume (int): The new volume level (0-100).
        """
        try:
            if not self.voice_client:
                await ctx.send("The bot is not currently playing music.")
                return

            if volume < 0 or volume > 100:
                await ctx.send("Volume must be between 0 and 100.")
                return

            # Set the new volume
            await self.music_player.set_volume(self.voice_client, volume / 100)
            await ctx.send(f"Volume set to {volume}%")

        except Exception as e:
            await ctx.send(f"An error occurred while setting the volume: {e}")

def setup(bot):
    """Setup function for the MusicCog."""
    bot.add_cog(MusicCog(bot))