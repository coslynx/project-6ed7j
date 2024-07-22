import lyricsgenius
from music_bot.config import GENIUS_API_KEY

class LyricsGetter:
    """
    A class to fetch lyrics using the Genius API.
    """
    def __init__(self):
        self.genius = lyricsgenius.Genius(GENIUS_API_KEY)

    def get_lyrics(self, song_title, artist_name):
        """
        Fetches lyrics for a given song and artist.

        Args:
            song_title (str): The title of the song.
            artist_name (str): The name of the artist.

        Returns:
            str: The lyrics of the song, or None if not found.
        """
        try:
            song = self.genius.search_song(song_title, artist_name)
            if song:
                return song.lyrics
            else:
                return None
        except Exception as e:
            print(f"Error fetching lyrics: {e}")
            return None