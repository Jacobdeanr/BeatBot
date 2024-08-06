# Discord Music Bot

A Discord bot that streams audio from YouTube into voice channels. This bot is built using `discord.py` and `pytubefix`.

## Features

- Join and leave voice channels
- Play, pause, resume, and skip songs
- Queue management
- Supports YouTube streaming

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Jacobdeanr/Beat-Bot.git
    cd beat-bot/src
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## Setup

### Discord Bot

1. Create a new application in the [Discord Developer Portal](https://discord.com/developers/applications) and add a bot to it.
2. Copy your bot token.
3. Create a `.env` file in the root directory of your project and add your bot token:

    ```env
    DISCORD_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
    ```

### Spotify Developer Account

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and log in with your Spotify account.
2. Click on "Create an App" and fill out the required details.
3. Once the app is created, you will see your `Client ID` and `Client Secret`. Add these to your `.env` file:

    ```env  
    SPOTIFY_CLIENT_ID=YOUR_SPOTIFY_CLIENT_ID
    SPOTIFY_CLIENT_SECRET=YOUR_SPOTIFY_CLIENT_SECRET
    ```

## Running the Bot

To run the bot, execute the following command:

```bash
python discordbot.py