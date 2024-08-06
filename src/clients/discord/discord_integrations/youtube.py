from typing import Union
import discord
from discord.ext import commands
from .shared import SharedIntegration

import asyncio
from concurrent.futures import ThreadPoolExecutor

from services.youtube.youtube_service import YouTubeService

from clients.discord.discord_messages.discord_views.queue_selected_view import QueueSelectedView
from clients.discord.discord_messages.discord_embed.services_embeds import YoutubeEmbedCreator

#from typing import TYPE_CHECKING, Union
#if TYPE_CHECKING:
from pytubefix import YouTube, Playlist, Channel, Stream


class YoutubeIntegration:
    def __init__(self, youtube_service):
        self.youtube_service: YouTubeService = youtube_service

    async def handle_request(self, ctx: commands.Context, request: str, fast_mode = False):
        """
        Handles YouTube requests from the user.

        Args:
            ctx (commands.Context): The command context.
            youtube_service (YouTubeService): The YouTube service instance.
            request (str): The user's request.
            search_limit (int, optional): The maximum number of search results to display. Defaults to 4.
            fast_mode (bool, optional): Whether to immediately add the request to the queue. Defaults to False.

        Returns:
            None
        """
        #Throw the request into the queue immediately as a youtube object, assuming it doesn't
        if fast_mode:
            result_list = self.youtube_service.search_and_bind(request,limit=1)
            result = result_list[0]

            if result.age_restricted:
                return None, None
            return 'add_to_queue', [result]
        
        search_limit: int = 4
        result, embed = await self.parse_link(ctx, request, search_limit)
        if result is None:
            return None, None

        view = QueueSelectedView(ctx, result)
        view.message = await ctx.send(view=view, embed=embed, content=f"{ctx.author.mention} Requested {request}")
        await view.wait()

        return view.user_choice, result
    
    def search_string(self, request: str, limit=4) -> list[YouTube]:
        return self.youtube_service.search_and_bind(request,limit=limit)

    def parse_link(self, request: str) -> 'Union[YouTube, Playlist]':
        """
    	Handles YouTube requests from the user.

        Args:
            request (str): The user's request.
        
        Returns:
            Union[YouTube, Playlist]: The search result.
        """

        if "playlist" in request or "list" in request:
            #print(f"Handling playlist {request}")
            result:Playlist = self.youtube_service.get_playlist_from_url(request)
            if not result:
                raise Exception(f"No items in playlist {request}")

        elif "watch" in request or "https://youtu.be/" in request:
            #print(f"watch {request}")
            result:'YouTube' = self.youtube_service.get_youtube_by_url(request)
            if result.age_restricted:
                raise Exception(f"{result.title} is age restricted.")
            
        else:
            raise Exception(f"Unable to parse YouTube link. Please provide a query.")
            

        #else:
        #    print(f"searching manually for {request}")
        #    result_list:list[YouTube] = self.youtube_service.search_and_bind(request,limit=search_limit)
        #    if result_list is None:
        #        return None, None
        #    
        #    # Not the most graceful, but the embed creator can't dynamically make buttons.
        #    if len(result_list) < 4:
        #        return None, None
        #    
        #    # If anything is age restricted we need to exit out...
        #    for item in result_list:
        #        if item.age_restricted:
        #            return None, None
#
        #    result = await SharedIntegration.handle_search_results(ctx, result_list, YoutubeEmbedCreator.create_video_search_embed)
        #    if result is None:
        #        return None, None
#
        #    embed = YoutubeEmbedCreator.create_video_embed(result)
        #    result = [result]

        return result

    #TODO: Figure out how to get this to work consistently with the search limits.  Will be needed for multiple items in the queue.
    async def fast_youtube_search(self, list_of_requests: list[str]) -> list[str]:
        print("performing fast search")
        result_urls: list = []

        # Get the event loop
        loop = asyncio.get_event_loop()

        # Create a thread pool executor
        executor = ThreadPoolExecutor(max_workers=2)  # Adjust the number of workers as needed

        async def fetch_url(request):
            query_result = await loop.run_in_executor(executor, self.youtube_service.perform_search, request, 1)
            if query_result is not None:
                if "https://www.youtube.com" in query_result:
                    return query_result
                url = f"https://www.youtube.com{query_result[0]['url_suffix']}"
                return url
            return None

        tasks = [fetch_url(request) for request in list_of_requests]
        results = await asyncio.gather(*tasks)
        result_urls = [result for result in results if result is not None]
        
        return result_urls

    def create_info_embed(self, video: 'YouTube'):
        return YoutubeEmbedCreator.create_video_embed(video)
    
    def create_search_safe_list(self, media_object: 'Union[YouTube, Playlist]') -> 'list[YouTube]':
        if isinstance(media_object, YouTube):
            return [media_object]
        elif isinstance(media_object, Playlist):
            return media_object.videos
        else:
            raise Exception(f"Invalid media object: {media_object}")