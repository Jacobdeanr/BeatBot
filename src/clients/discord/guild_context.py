import discord

class GuildContext:
    def __init__(self, bot, guild_id, guild_queue, audio_player, voice_client):
        self.bot = bot
        self.guild_id = guild_id
        self.guild_queue = guild_queue
        self.audio_player = audio_player
        self.voice_client = voice_client