import discord
import asyncio
import enum


class DiscordGuildAudioPlayer:
    def __init__(self, guild_id, vc, on_song_end_callback=None):
        self.guild_id = guild_id
        self.voice_client: discord.VoiceClient = vc
        self.on_song_end_callback = on_song_end_callback
        self.loop = asyncio.get_running_loop()

    def play_stream(self, stream_url: str) -> None:
        """
        A method to play a stream in the voice channel.
        
        Parameters:
            source (str): The source of the audio stream.
        
        Returns:
            None
        """
        if self.voice_client.is_playing():
            #If we're already playing, exit early
            return
        
        if self.voice_client.is_paused():
            #If we're paused, exit early
            return
        
        try:
            audio_source = discord.FFmpegPCMAudio(stream_url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", options="-vn", executable="ffmpeg")
            self.voice_client.play(audio_source, after=self.after_song_ends)
        except Exception as e:
            print(f"\tError playing audio: {e}")
                
    def play_file(self, song_file: str) -> None:
        """
        Play a song file using the provided song file path and song information dictionary.

        Args:
            song_file (str): The file path of the song to be played.

        Returns:
            None
        """
        if not self.voice_client.is_playing():
            try:
                audio_source = discord.FFmpegPCMAudio(song_file, executable="ffmpeg")
                self.voice_client.play(audio_source, after=self.after_song_ends)
            except Exception as e:
                print(f"\tError playing audio: {e}")

    def after_song_ends(self, error=None) -> None:
        """
        A function that handles actions after a song ends.

        :param error: An optional parameter representing any error that occurred.
        :return: None
        """
        if self.on_song_end_callback:
            try:
                asyncio.run_coroutine_threadsafe(self.on_song_end_callback(self.guild_id, self.voice_client, error), self.loop).result()
            except Exception as e:
                print(f"Error in after_song_ends: {e}")

    def stop(self) -> bool:
        """
        Stop the playback if it is currently active.
        """
        if not self.voice_client:
            #This should probably be an exception. Returning False for now.
            return False
        
        if self.voice_client.is_playing():
            try:
                self.voice_client.stop()
                if not self.voice_client.is_playing():
                    return True
            except Exception as e:
                print(f"Error in stop: {e}")
                return False
    
    def pause(self) -> bool:
        """
        A method to pause the playback if a voice client exists.
        No parameters are required.
        Returns None.
        """
        if not self.voice_client:
            #This should probably be an exception. Returning False for now.
            return False
        
        if self.voice_client.is_playing():
            try:
                self.voice_client.pause()
                if self.voice_client.is_paused():
                    return True
            except Exception as e:
                print(f"Error in pause: {e}")
                return False
    
    def resume(self) -> bool:
        """
        A method to resume playback if there is a voice client available.
        """
        if not self.voice_client:
            return False
        
        if self.voice_client.is_paused():
            try:
                self.voice_client.resume()
                if self.voice_client.is_playing():
                    return True
            except Exception as e:
                print(f"Error in resume: {e}")
                return False
        