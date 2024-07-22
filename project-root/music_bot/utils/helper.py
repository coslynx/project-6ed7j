import discord

def format_song_info(song_info):
    """Formats song information for display in embeds.

    Args:
        song_info (dict): A dictionary containing song information (title, artist, duration).

    Returns:
        str: A formatted string containing the song information.
    """
    title = song_info.get('title', 'Unknown Title')
    artist = song_info.get('artist', 'Unknown Artist')
    duration = song_info.get('duration', 'Unknown Duration')

    # Format duration in HH:MM:SS format
    duration_string = get_current_time_string(duration)

    return f"{title} by {artist} ({duration_string})"

def get_current_time_string(seconds):
    """Converts seconds to a time string in the format "HH:MM:SS".

    Args:
        seconds (int): The number of seconds.

    Returns:
        str: The formatted time string.
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def get_song_duration(song_url):
    """Retrieves the duration of a song from its URL.

    Args:
        song_url (str): The URL of the song.

    Returns:
        int: The duration of the song in seconds.
    """
    # Implement logic to extract duration from the song URL
    # This will vary depending on the music source (YouTube, Spotify, SoundCloud)
    # Example for YouTube using youtube_dl:
    try:
        with youtube_dl.YoutubeDL({'format': 'bestaudio'}) as ydl:
            info = ydl.extract_info(song_url, download=False)
            duration = info['duration']
            return duration
    except Exception as e:
        print(f"Error getting song duration: {e}")
        return None

def get_song_title(song_url):
    """Extracts the title of a song from its URL.

    Args:
        song_url (str): The URL of the song.

    Returns:
        str: The title of the song.
    """
    # Implement logic to extract the title from the song URL
    # This will vary depending on the music source
    # Example for YouTube using youtube_dl:
    try:
        with youtube_dl.YoutubeDL({'format': 'bestaudio'}) as ydl:
            info = ydl.extract_info(song_url, download=False)
            title = info['title']
            return title
    except Exception as e:
        print(f"Error getting song title: {e}")
        return None

def get_song_artist(song_url):
    """Extracts the artist of a song from its URL.

    Args:
        song_url (str): The URL of the song.

    Returns:
        str: The artist of the song.
    """
    # Implement logic to extract the artist from the song URL
    # This will vary depending on the music source
    # Example for YouTube using youtube_dl:
    try:
        with youtube_dl.YoutubeDL({'format': 'bestaudio'}) as ydl:
            info = ydl.extract_info(song_url, download=False)
            artist = info['uploader']
            return artist
    except Exception as e:
        print(f"Error getting song artist: {e}")
        return None