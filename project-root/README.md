# MusicBot

This repository contains the source code for a Discord music bot. The bot allows users to play music from YouTube, Spotify, and SoundCloud within Discord voice channels.

## Features

* **Music Playback:** Play music from YouTube, Spotify, and SoundCloud.
* **Queue Management:** Add songs to a queue, skip songs, and see the current queue.
* **Voice Channel Integration:** Join and leave voice channels seamlessly.
* **Volume Control:** Adjust the playback volume.
* **Playlist Management:** Create, manage, and share playlists.
* **Lyrics Display:** Display lyrics for the currently playing song.
* **Admin Commands:** Set the command prefix, set the default music source, and reload cogs.

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/music-bot.git
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Create a .env file:** Copy the `.env.example` file and rename it to `.env`. Fill in the required API keys and bot token.

4. **Run the bot:**
```bash
python main.py
```

## Usage

1. **Invite the bot to your server:**
   - Go to the bot's application page on Discord Developer Portal.
   - Click on "OAuth2" in the left sidebar.
   - Select the "bot" scope and check the "Send Messages" and "Connect" permissions.
   - Copy the generated URL and paste it into your browser.
   - Choose the server you want to add the bot to.

2. **Use the following commands:**

   | Command           | Description                                                              |
   |-------------------|-----------------------------------------------------------------------|
   | `/play [query]`    | Plays a song from YouTube, Spotify, or SoundCloud.                      |
   | `/skip`           | Skips the current song in the queue.                                     |
   | `/stop`           | Stops the current playback and clears the queue.                          |
   | `/pause`          | Pauses the current playback.                                             |
   | `/resume`         | Resumes the paused playback.                                             |
   | `/queue`          | Displays the current music queue.                                      |
   | `/volume [level]`  | Adjusts the playback volume.                                           |
   | `/createplaylist [name]` | Creates a new playlist.                                           |
   | `/addsong [playlist name] [song URL]` | Adds a song to a playlist.                              |
   | `/removesong [playlist name] [song URL]` | Removes a song from a playlist.                      |
   | `/deleteplaylist [name]` | Deletes a playlist.                                              |
   | `/shareplaylist [playlist name]` | Shares a playlist with the server.                          |
   | `/saveplaylist [playlist name]` | Saves a playlist for future use.                            |
   | `/loadplaylist [playlist name]` | Loads a saved playlist.                                    |
   | `/lyrics`         | Displays the lyrics for the currently playing song.                      |

3. **Admin commands:**

   | Command             | Description                                                              |
   |---------------------|-----------------------------------------------------------------------|
   | `/setprefix [prefix]` | Sets a new command prefix for the bot.                               |
   | `/setsource [source]` | Sets the default music source (YouTube, Spotify, or SoundCloud).      |
   | `/reload`            | Reloads the bot's cogs.                                                |

## Deployment

1. **Create a Heroku account:** Go to [https://www.heroku.com/](https://www.heroku.com/) and sign up for a free account.

2. **Create a new Heroku app:**
   - Click on the "New" button and select "Create new app".
   - Choose a unique app name and select a region.

3. **Connect the repository to Heroku:**
   - Click on the "Deploy" tab.
   - Choose "GitHub" as the deployment method.
   - Search for the repository and connect it to the Heroku app.

4. **Configure the environment variables:**
   - Click on the "Settings" tab.
   - Click on "Reveal Config Vars".
   - Add the environment variables from your `.env` file.

5. **Deploy the bot:**
   - Click on the "Deploy" tab.
   - Choose the branch you want to deploy from.
   - Click on "Deploy Branch".

6. **Start the bot:**
   - After deployment is complete, you can start the bot by clicking on the "Open App" button.

## Contributing

Contributions are welcome! If you have any ideas or suggestions, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.