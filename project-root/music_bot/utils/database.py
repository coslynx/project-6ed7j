import sqlite3
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
DATABASE_NAME = os.getenv('DATABASE_NAME')

class Database:
    """
    A class to manage database interactions.

    Supports both SQLite and MongoDB.
    """

    def __init__(self):
        if DATABASE_URL.startswith('sqlite'):
            self.connection = sqlite3.connect(DATABASE_URL)
            self.create_tables()
        elif DATABASE_URL.startswith('mongodb'):
            self.client = pymongo.MongoClient(DATABASE_URL)
            self.db = self.client[DATABASE_NAME]
        else:
            raise ValueError("Invalid database URL. Choose SQLite or MongoDB.")

    def create_tables(self):
        """
        Creates the required tables in the SQLite database.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS playlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                songs TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                preference_name TEXT NOT NULL,
                preference_value TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bot_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_name TEXT NOT NULL,
                setting_value TEXT
            )
        """)
        self.connection.commit()

    def create_playlist(self, playlist_name, user_id):
        """
        Creates a new playlist in the database.

        Args:
            playlist_name (str): The name of the playlist.
            user_id (int): The ID of the user creating the playlist.
        """
        if DATABASE_URL.startswith('sqlite'):
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO playlists (name, user_id, songs) VALUES (?, ?, '')", (playlist_name, user_id))
            self.connection.commit()
        elif DATABASE_URL.startswith('mongodb'):
            self.db.playlists.insert_one({"name": playlist_name, "user_id": user_id, "songs": []})

    def add_song_to_playlist(self, playlist_name, song_url, user_id):
        """
        Adds a song to an existing playlist.

        Args:
            playlist_name (str): The name of the playlist.
            song_url (str): The URL of the song to add.
            user_id (int): The ID of the user adding the song.
        """
        if DATABASE_URL.startswith('sqlite'):
            cursor = self.connection.cursor()
            cursor.execute("SELECT songs FROM playlists WHERE name = ? AND user_id = ?", (playlist_name, user_id))
            songs = cursor.fetchone()[0]
            if songs:
                songs += f"{song_url},"
            else:
                songs = f"{song_url},"
            cursor.execute("UPDATE playlists SET songs = ? WHERE name = ? AND user_id = ?", (songs, playlist_name, user_id))
            self.connection.commit()
        elif DATABASE_URL.startswith('mongodb'):
            self.db.playlists.update_one(
                {"name": playlist_name, "user_id": user_id},
                {"$push": {"songs": song_url}}
            )

    def remove_song_from_playlist(self, playlist_name, song_url, user_id):
        """
        Removes a song from a playlist.

        Args:
            playlist_name (str): The name of the playlist.
            song_url (str): The URL of the song to remove.
            user_id (int): The ID of the user removing the song.
        """
        if DATABASE_URL.startswith('sqlite'):
            cursor = self.connection.cursor()
            cursor.execute("SELECT songs FROM playlists WHERE name = ? AND user_id = ?", (playlist_name, user_id))
            songs = cursor.fetchone()[0]
            if songs:
                songs = songs.replace(f"{song_url},", "")
                songs = songs.replace(f"{song_url}", "")
            cursor.execute("UPDATE playlists SET songs = ? WHERE name = ? AND user_id = ?", (songs, playlist_name, user_id))
            self.connection.commit()
        elif DATABASE_URL.startswith('mongodb'):
            self.db.playlists.update_one(
                {"name": playlist_name, "user_id": user_id},
                {"$pull": {"songs": song_url}}
            )

    def delete_playlist(self, playlist_name, user_id):
        """
        Deletes a playlist.

        Args:
            playlist_name (str): The name of the playlist to delete.
            user_id (int): The ID of the user deleting the playlist.
        """
        if DATABASE_URL.startswith('sqlite'):
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM playlists WHERE name = ? AND user_id = ?", (playlist_name, user_id))
            self.connection.commit()
        elif DATABASE_URL.startswith('mongodb'):
            self.db.playlists.delete_one({"name": playlist_name, "user_id": user_id})

    def get_playlist(self, playlist_name, user_id):
        """
        Retrieves a playlist from the database.

        Args:
            playlist_name (str): The name of the playlist to retrieve.
            user_id (int): The ID of the user who owns the playlist.

        Returns:
            list: A list of song URLs in the playlist, or None if the playlist is not found.
        """
        if DATABASE_URL.startswith('sqlite'):
            cursor = self.connection.cursor()
            cursor.execute("SELECT songs FROM playlists WHERE name = ? AND user_id = ?", (playlist_name, user_id))
            songs = cursor.fetchone()
            if songs:
                return songs[0].split(',')[:-1]  # Remove trailing comma
            else:
                return None
        elif DATABASE_URL.startswith('mongodb'):
            playlist = self.db.playlists.find_one({"name": playlist_name, "user_id": user_id})
            if playlist:
                return playlist["songs"]
            else:
                return None

    def get_all_playlists(self, user_id):
        """
        Retrieves all playlists associated with a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: A list of playlist names.
        """
        if DATABASE_URL.startswith('sqlite'):
            cursor = self.connection.cursor()
            cursor.execute("SELECT name FROM playlists WHERE user_id = ?", (user_id,))
            return [row[0] for row in cursor.fetchall()]
        elif DATABASE_URL.startswith('mongodb'):
            playlists = self.db.playlists.find({"user_id": user_id})
            return [playlist["name"] for playlist in playlists]

    def set_user_preference(self, user_id, preference_name, preference_value):
        """
        Updates a user's preference.

        Args:
            user_id (int): The ID of the user.
            preference_name (str): The name of the preference.
            preference_value (str): The value of the preference.
        """
        if DATABASE_URL.startswith('sqlite'):
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO user_preferences (user_id, preference_name, preference_value) VALUES (?, ?, ?)",
                (user_id, preference_name, preference_value)
            )
            self.connection.commit()
        elif DATABASE_URL.startswith('mongodb'):
            self.db.user_preferences.update_one(
                {"user_id": user_id, "preference_name": preference_name},
                {"$set": {"preference_value": preference_value}},
                upsert=True  # Create the document if it doesn't exist
            )

    def get_user_preference(self, user_id, preference_name):
        """
        Retrieves a user's preference.

        Args:
            user_id (int): The ID of the user.
            preference_name (str): The name of the preference.

        Returns:
            str: The value of the preference, or None if not found.
        """
        if DATABASE_URL.startswith('sqlite'):
            cursor = self.connection.cursor()
            cursor.execute("SELECT preference_value FROM user_preferences WHERE user_id = ? AND preference_name = ?", (user_id, preference_name))
            preference = cursor.fetchone()
            if preference:
                return preference[0]
            else:
                return None
        elif DATABASE_URL.startswith('mongodb'):
            preference = self.db.user_preferences.find_one({"user_id": user_id, "preference_name": preference_name})
            if preference:
                return preference["preference_value"]
            else:
                return None

    def set_bot_setting(self, setting_name, setting_value):
        """
        Updates a bot setting.

        Args:
            setting_name (str): The name of the setting.
            setting_value (str): The value of the setting.
        """
        if DATABASE_URL.startswith('sqlite'):
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO bot_settings (setting_name, setting_value) VALUES (?, ?)",
                (setting_name, setting_value)
            )
            self.connection.commit()
        elif DATABASE_URL.startswith('mongodb'):
            self.db.bot_settings.update_one(
                {"setting_name": setting_name},
                {"$set": {"setting_value": setting_value}},
                upsert=True  # Create the document if it doesn't exist
            )

    def get_bot_setting(self, setting_name):
        """
        Retrieves a bot setting.

        Args:
            setting_name (str): The name of the setting.

        Returns:
            str: The value of the setting, or None if not found.
        """
        if DATABASE_URL.startswith('sqlite'):
            cursor = self.connection.cursor()
            cursor.execute("SELECT setting_value FROM bot_settings WHERE setting_name = ?", (setting_name,))
            setting = cursor.fetchone()
            if setting:
                return setting[0]
            else:
                return None
        elif DATABASE_URL.startswith('mongodb'):
            setting = self.db.bot_settings.find_one({"setting_name": setting_name})
            if setting:
                return setting["setting_value"]
            else:
                return None

    def close(self):
        """
        Closes the database connection.
        """
        if DATABASE_URL.startswith('sqlite'):
            self.connection.close()
        elif DATABASE_URL.startswith('mongodb'):
            self.client.close()