import os
from dotenv import load_dotenv

load_dotenv()

# Bot Token
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Music Source APIs
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SOUNDCLOUD_CLIENT_ID = os.getenv('SOUNDCLOUD_CLIENT_ID')
SOUNDCLOUD_CLIENT_SECRET = os.getenv('SOUNDCLOUD_CLIENT_SECRET')

# Lyrics API
GENIUS_API_KEY = os.getenv('GENIUS_API_KEY')

# Database Settings
# For SQLite:
# DATABASE_URL = 'sqlite:///musicbot.db' 

# For MongoDB:
# DATABASE_URL = 'mongodb://localhost:27017/'
# DATABASE_NAME = 'musicbot'

# Default Command Prefix
COMMAND_PREFIX = '/'

# Default Music Source
DEFAULT_MUSIC_SOURCE = 'youtube' 

# Bot Activity (e.g., 'listening to music', 'playing music')
ACTIVITY_TYPE = discord.ActivityType.listening
ACTIVITY_NAME = 'music'

# Logging Level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOGGING_LEVEL = logging.INFO

# Other Settings (Optional)
# - Playlist Saving/Loading Settings (e.g., file path)
# - Audio Filters (e.g., bass boost, equalizer settings)
# - Additional Features (e.g., random shuffle, looping)