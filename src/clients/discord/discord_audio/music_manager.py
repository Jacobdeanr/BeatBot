import discord
from clients.discord.discord_audio.queue.guild_queue_manager import GuildQueueManager
from clients.discord.discord_audio.queue.queue_item import QueueItem
from clients.discord.discord_audio.audio.discord_guild_audio_player_manager import DiscordGuildAudioPlayerManager
from clients.discord.discord_audio.audio.dicord_voice_connecter import DiscordVoiceConnecter

class MusicManager:
    def __init__(self, bot):
        self.bot: discord.Client = bot
        self.guild_queue_manager = GuildQueueManager()
        self.voice_client_connecter = DiscordVoiceConnecter()
        self.guild_audio_player_manager = DiscordGuildAudioPlayerManager()
    
    #Queue Management
    def get_guild_queue(self, guild_id) -> list:
        """
        Get the queue for a specific guild.

        Args:
            guild_id (int): The ID of the guild.

        Returns:
            queue: The queue for the specified guild.
        """
        return self.guild_queue_manager.get_guild_queue_by_id(guild_id).queue

    def clear_queue(self, guild_id) -> bool:
        """
        Clears the queue for a specific guild identified by the given guild_id.

        Parameters:
            guild_id (int): The ID of the guild whose queue needs to be cleared.

        Returns:
            bool: True if the guild queue was successfully cleared, False otherwise.
        """
        try:
            self.guild_queue_manager.clear_guild_queue_by_id(guild_id)
            return True
        except Exception as e:
            print(f"Error clearing guild queue: {e}")
            return False
    
    def add_item_to_queue(self, guild_id, queue_item:QueueItem) -> None:
        """
        Add an item to the queue of a specific guild.

        Parameters:
            guild_id (int): The ID of the guild to add the item to.
            item (any): The item to add to the queue.
            position (int, optional): The position in the queue to add the item to. Defaults to None.
        """
        try:
            self.guild_queue_manager.get_guild_queue_by_id(guild_id)
            self.guild_queue_manager.add_item_to_guild_queue_by_id_end(guild_id, queue_item)
        except Exception as e:
            print(f"Error adding item to queue: {e}")

    async def play_queue_in_channel(self, guild_id: int, channel_id: int) -> bool:
        """
        An asynchronous function that adds an item to the queue and plays it in the voice channel.

        Parameters:
            guild_id (int): The ID of the guild.
            channel_id (int): The ID of the channel to play the item in.

        Returns:
            bool: True if the item was successfully added and played, False otherwise.
        """
        try:
            vc: discord.VoiceClient = await self._connect_to_voice_channel(guild_id, channel_id)
            if vc is not None:
                if not vc.is_playing():
                    await self._play_next_song(guild_id, vc)
        except Exception as e:
            print(f"Error adding item to queue: {e}")

    def get_current_song(self, guild_id) -> str:
        """
        Get the current song for a given guild.

        Args:
            guild_id (int): The ID of the guild to get the current song for.

        Returns:
            str: The current song for the specified guild.
        """
        return self.guild_queue_manager.get_current_song_by_id(guild_id)

    def _set_current_song(self, guild_id, queue_item: QueueItem) -> None:
        """
        Set the current song for a given guild.

        Parameters:
            guild_id (int): The ID of the guild where the song is being set.
            item (str): The item representing the current song.

        Returns:
            None
        """
        self.guild_queue_manager.set_current_song_by_id(guild_id, queue_item)
    
    #Helpers for play
    def _play_stream(self, guild_id, voice_client, stream_url) -> None:
        """
        Determine whether to play from a local file or stream, and get the appropriate source
        song_to_play: str - The path or stream of the song to be played
        guild_id: int - The ID of the guild where the song will be played
        voice_client: VoiceClient - The client handling voice connections
        song_info: dict - Information about the song being played
        """
        dap = self.guild_audio_player_manager.get_audio_player_by_id(guild_id, voice_client, self._song_end_callback)

        dap.play_stream(stream_url)

    async def _song_end_callback(self, guild_id, voice_client, error=None) -> None:
        """
        A callback function that is triggered when a song ends in the music player.
        
        Parameters:
            guild_id (int): The ID of the guild where the song ended.
            voice_client: The voice client to interact with for playing the next song.
            error (Exception, optional): Any error that occurred during playback.
        
        Returns:
            None
        """
        if error:
            print(error)
            return
        
        quild_queue = self.guild_queue_manager.get_guild_queue_by_id(guild_id)
        if len(quild_queue.queue) == 0:
            return
        
        stream_url = None
        try:
            while stream_url is None:
                next_song: QueueItem = self.guild_queue_manager.pop_item_from_guild_queue_by_id(guild_id, 0)

                if next_song:
                    stream_url = await next_song.get_stream_url()
                break

            self._play_stream(guild_id, voice_client, stream_url)
            self._set_current_song(guild_id, next_song)
        except Exception as e:
            print(f"Error in song_end_callback to play next song: {e}")

    #Playback
    async def _play_next_song(self, guild_id: int, voice_client: discord.VoiceClient) -> None:
        """
        Attempts to play the next song in the queue for a given guild.

        Parameters:
        - guild_id: The ID of the guild where the song will be played.
        - voice_client: The Discord voice client for audio playback.

        Returns:
        - True if a song was successfully started. False otherwise.
        """
        quild_queue = self.guild_queue_manager.get_guild_queue_by_id(guild_id)
        if len(quild_queue.queue) == 0:
            raise Exception("No songs in queue")
        
        while True:
            next_song: QueueItem = self.guild_queue_manager.pop_item_from_guild_queue_by_id(guild_id, 0)

            if next_song:
                stream_url = await next_song.get_stream_url()
            break

        self._play_stream(guild_id, voice_client, stream_url)
        self._set_current_song(guild_id, next_song)
    
    def get_guild_voice_client(self, guild_id: int) -> discord.VoiceClient:
        guild = self.bot.get_guild(guild_id)
        return guild.voice_client
    
    def _stop_audio_player(self, guild_id: int) -> bool:
        """
        Stops the audio player for the given guild ID.

        Parameters:
            guild_id (int): The ID of the guild for which to stop the audio player.

        Returns:
            None
        """
        return self.guild_audio_player_manager.stop_audio_player_by_id(guild_id)

    def stop_playback(self, guild_id: int) ->  None:
        """
        Stops the audio playback for the specified guild.

        Args:
            guild_id (int): The ID of the guild to stop audio playback for.

        Returns:
            bool: True if the audio playback was stopped successfully, False otherwise.
        """
        try:
            if self.get_guild_voice_client(guild_id):
                self._stop_audio_player(guild_id)
        except Exception as e:
            print(f"Error stopping audio playback for guild {guild_id}: {e}")

    def pause_playback(self, guild_id) -> None:
        """
        Pauses the playback for the given guild ID.

        Args:
            guild_id: The ID of the guild for which the playback is to be paused (str).

        Returns:
            bool: True if the playback was successfully paused, False otherwise.
        """
        try:
            if self.get_guild_voice_client(guild_id):
                self.guild_audio_player_manager.pause_audio_player_by_id(guild_id)
                return True
        except Exception as e:
            print(f"Error pausing playback for guild {guild_id}: {e}")
            return False

    def resume_playback(self, guild_id) -> None:
        """
        A function to resume playback in the audio player for a specific guild.

        Parameters:
            guild_id (int): The ID of the guild to resume playback for.

        Returns:
            bool: True if playback was successfully resumed, False otherwise.
        """
        try:
            if self.get_guild_voice_client(guild_id):
                return self.guild_audio_player_manager.resume_audio_player_by_id(guild_id)
        except Exception as e:
            print(f"Error resuming playback for guild {guild_id}: {e}")
            return False
    
    def skip_playback(self, guild_id) -> bool:
        """
        Skips the current song being played in the audio player for the given guild ID.

        Args:
            guild_id (str): The ID of the guild for which the song needs to be skipped.

        Returns:
            bool: True if the song was successfully skipped, False otherwise.
        """
        try:
            if self.get_guild_voice_client(guild_id):
                return self._stop_audio_player(guild_id)
        except Exception as e:
            print(f"Error skipping song for guild {guild_id}: {e}")
            return False
        
    #Connections
    async def _connect_to_voice_channel(self, guild_id:int, voice_channel_id:int) -> discord.VoiceClient:
        """
        Connects to a voice channel in the specified guild and returns a VoiceClient object.

        Parameters:
            guild_id (int): The ID of the guild to connect to.
            channel_id (int): The ID of the voice channel to connect to.

        Returns:
            discord.VoiceClient: A reference to the VoiceClient object representing the connection.
        """
        
        guild: discord.Guild = self.bot.get_guild(guild_id)
        if not guild.voice_client:
            try:
                voice_channel = guild.get_channel(voice_channel_id)
                return await self.voice_client_connecter.connect_to_voice_channel(voice_channel)
            except Exception as e:
                print(f"Error connecting to voice channel: {e}")
        return guild.voice_client

    async def join_voice_channel(self, guild_id, voice_channel_id) -> None:
        """
        A function to join a voice channel in the audio player for a specific guild.

        Parameters:
            guild_id (int): The ID of the guild to join the voice channel for.
            voice_channel_id (int): The ID of the voice channel to join.

        Returns:
            bool: True if the voice channel was successfully joined, False otherwise.
        """
        try:
            return await self._connect_to_voice_channel(guild_id, voice_channel_id)
        except Exception as e:
            print(f"Error joining voice channel for guild {guild_id}: {e}")
            return None

    async def disconnect_from_guild(self, guild_id) -> None:
        """
        An asynchronous function to disconnect the bot from a specified guild's voice channel.
        
        Parameters:
            guild_id (int): The unique identifier of the guild to disconnect from.
        
        Returns:
            bool: True if the bot successfully disconnects, False otherwise.
        """
        try:
            guild: discord.Guild = self.bot.get_guild(guild_id)
            self.clear_queue(guild_id)
            self.stop_playback(guild_id)
            await self.voice_client_connecter.disconnect_from_guild(guild.voice_client)
            return True
        except Exception as e:
            print(f"Error disconnecting from voice channel for guild {guild_id}: {e}")
            return False