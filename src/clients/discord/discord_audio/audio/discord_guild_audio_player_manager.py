import discord
from asyncio import Lock
from .discord_guild_audio_player import DiscordGuildAudioPlayer

class DiscordGuildAudioPlayerManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DiscordGuildAudioPlayerManager, cls).__new__(cls, *args, **kwargs)
            cls.audio_players = {}
        return cls._instance
    
    def get_audio_player_by_id(self, guild_id: int, voice_client: discord.VoiceClient, on_song_end_callback=None) -> DiscordGuildAudioPlayer:
        """
        Retrieves the audio player associated with the given guild ID. If the guild ID is not present in the audio players dictionary, a new DiscordAudioPlayer is created and stored. Returns the DiscordAudioPlayer associated with the given guild ID.
        
        Parameters:
            guild_id (int): The ID of the guild.
            vc: The voice channel associated with the guild.
            on_song_end_callback (optional): Callback function to be executed when a song ends.
        
        Returns:
            DiscordAudioPlayer: The audio player associated with the given guild ID.
        """
        if (guild_id not in self.audio_players) or (self.audio_players[guild_id].voice_client != voice_client):
            self.audio_players[guild_id] = self._create_audio_player(guild_id, voice_client, on_song_end_callback=on_song_end_callback)
        return self.audio_players[guild_id]
    
    def find_audio_player_by_id(self, guild_id: int) -> DiscordGuildAudioPlayer:
        """
        Find and return the DiscordGuildAudioPlayer associated with the provided guild_id.
        
        Parameters:
            guild_id (int): The ID of the guild to search for.
            
        Returns:
            DiscordGuildAudioPlayer: The audio player associated with the guild_id if found, otherwise None.
        """
        if guild_id in self.audio_players:
            return self.audio_players[guild_id]
    
    def _create_audio_player(self, guild_id: int, voice_client: discord.VoiceClient, on_song_end_callback=None) -> DiscordGuildAudioPlayer:
        """
        Create an audio player for a specific guild using the provided voice client.
        
        Parameters:
            guild_id (int): The id of the guild for which the audio player is being created.
            voice_client (discord.VoiceClient): The voice client to use for audio playback.
            on_song_end_callback (callable): Optional callback function to handle when a song ends.
        
        Returns:
            DiscordGuildAudioPlayer: An instance of DiscordGuildAudioPlayer for the specified guild.
        """
        return DiscordGuildAudioPlayer(guild_id, voice_client, on_song_end_callback=on_song_end_callback)
    
    def stop_audio_player_by_id(self, guild_id: int) -> bool:
        """
        Stop the audio player for the specified guild ID.

        Parameters:
            guild_id (int): The ID of the guild for which the audio player should be stopped.

        Returns:
            None
        """
        if guild_id in self.audio_players:
            gap: DiscordGuildAudioPlayer = self.audio_players[guild_id]
            return gap.stop()

    def pause_audio_player_by_id(self, guild_id: int) -> bool:
        """
        Pause the audio player for a specific guild by its ID.

        Parameters:
            guild_id (int): The ID of the guild for which to pause the audio player.

        Returns:
            None
        """
        if guild_id in self.audio_players:
            return self.audio_players[guild_id].pause()
    
    def resume_audio_player_by_id(self, guild_id: int) -> bool:
        """
        Resumes the audio player for a specific guild based on the provided guild ID.
        
        Parameters:
            guild_id (int): The ID of the guild for which the audio player needs to be resumed.
        
        Returns:
            None
        """
        if guild_id in self.audio_players:
            return self.audio_players[guild_id].resume()
    
    def get_audio_player_state_by_id(self, guild_id: int) -> str:
        """
        Retrieve the playback state of the audio player for a specific guild.

        Parameters:
            guild_id (int): The ID of the guild to retrieve the audio player state for.

        Returns:
            str: The playback state of the audio player for the specified guild.
        """
        return self.audio_players[guild_id].playback_state