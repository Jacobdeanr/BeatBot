from typing import Union
import asyncio
from concurrent.futures import ThreadPoolExecutor
from discord.ext import commands

from services.youtube.youtube_service import YouTubeService

from pytubefix import YouTube
from services.spotify.tracks import SpotifyTrack

executor = ThreadPoolExecutor(max_workers=5)

class QueueItem:
    def __init__(self, source_object: 'Union[YouTube, SpotifyTrack]', ctx: commands.Context):
        """
        Initializes a QueueItem object with the given source object and context.
        
        Parameters:
            source_object (Union[YouTube, SpotifyTrack]): The source object associated with the queue item. Must be either a YouTube object or a SpotifyTrack object.
            ctx (commands.Context): The Discord context associated with the queue item.
        """
        self.source_object = source_object
        self.ctx = ctx
        self.yt_object:YouTube = None
        self.stream_url = None

    def __str__(self):
        return f"{self.source_object}"
    
    def __repr__(self):
        return f"{self.source_object}"

    async def notify_user(self, message):
        """
        Asynchronously sends a notification message in the context's channel.

        Parameters:
            message (str): The message to send to the channel from which the command was invoked.
        """
        try:
            await self.ctx.send(message)
        except Exception as e:
            print(f"Failed to send message: {e}")

    async def log_request(self):
        """
        Asynchronously logs the request for debugging or analytics, with detailed context info.
        """
        log_message = f"Item requested by {self.ctx.author.display_name} in '{self.ctx.guild.name}' via channel '{self.ctx.channel.name}'."
        print(log_message)

    async def get_stream_url(self) -> str:
        """
        Asynchronously retrieves the streaming URL for the source object.

        This function dynamically determines the type of the source object and delegates the stream retrieval
        to the appropriate method, handling SpotifyTrack and YouTube cases accordingly.

        Returns:
            The streaming URL of the source object obtained by invoking the respective method.
        """
        try:
            youtube_service = YouTubeService()
            loop = asyncio.get_running_loop()
            
            if not self.yt_object:
                await self._prepare_for_playback(youtube_service, loop)
                self.stream_url:str = await loop.run_in_executor(executor, youtube_service.get_audio_stream, self.yt_object)
            
            if self.stream_url:
                return self.stream_url
            
        except Exception as e:
            print(f"Failed to get stream URL: {e}")

    async def _prepare_for_playback(self, youtube_service: YouTubeService, loop: asyncio.AbstractEventLoop):
        match self.source_object:
            case SpotifyTrack():
                # Build the query for a Spotify track
                query = f"{self.source_object.artists[0].name} {self.source_object.name}"
            case str():
                # Use the string directly as a query
                query = self.source_object
            case YouTube():
                # Already a YouTube object, no need to search
                self.yt_object = self.source_object
                return
            case _:
                query = None

        # If we have a query, run the search
        if query:
            yt_object = await loop.run_in_executor(
                executor,
                youtube_service.search_and_bind,
                query,
                1
            )
            if yt_object:
                self.yt_object = yt_object[0]

#async def main():    
#    import time
#    start = time.perf_counter()
#    item = QueueItem(YouTube("https://www.youtube.com/watch?v=dQw4w9WgXcQ"), None)
#    try:
#        result = await item.get_stream_url()
#        print(result)
#    except Exception as e:
#        print(f"Failed to retrieve stream URL: {e}")
#    finally:
#        end = time.perf_counter()
#        print(f"Time to complete: {end - start:0.4f} seconds")
#
#if __name__ == "__main__":
#    loop = asyncio.new_event_loop()
#    asyncio.set_event_loop(loop)  # Set the new event loop as the current loop
#    loop.run_until_complete(main())
#    loop.close()  # Properly close the loop after completion