from typing import Union
import discord
from discord.ext import commands

from services.spotify.spotify_service import SpotifyService


from services.spotify.tracks import SpotifyTrack
from services.spotify.playlists import SpotifyPlaylist
from services.spotify.albums import SpotifyAlbum
from services.spotify.artists import SpotifyArtist

import random

from .shared import SharedIntegration
from clients.discord.discord_messages.discord_embed.services_embeds import SpotifyEmbedCreator

#QueueSelectedView
from clients.discord.discord_messages.discord_views.queue_selected_view import QueueSelectedView

class SpotifyIntegration:
    def __init__(self, spotify_service):
        self.spotify_service: SpotifyService = spotify_service

    async def handle_request(self, ctx: commands.Context, request: str) -> 'Union[SpotifyTrack, SpotifyPlaylist, SpotifyAlbum, SpotifyArtist, None]':
        """
        Handles Spotify requests from the user.

        Args:
            ctx (commands.Context): The command context.
            self.spotify_service (SpotifyService): The Spotify service instance.
            request (str): The user's request.
            search_limit (int, optional): The maximum number of search results to display. Defaults to 4.

        Returns:
            None
        """
        request = request.split("?")[0]

        #if not "spotify.com/" in request:
        #    results: list[SpotifyTrack] = self.spotify_service.perform_search(request, limit=search_limit)
        results = self.search_string(request)
        result = await SharedIntegration.handle_search_results(ctx, results, SpotifyEmbedCreator.create_song_search_embed)
        if result is None:
            raise ValueError("No results found")
        
        #embed = SpotifyEmbedCreator.create_track_embed(result)

        #search_safe_list = [f"{result.artists[0].name} - {result.name} lyrics"]
        #search_safe_list = [f"{result.artists[0].name} - {result.name}"]

        #else:
        #    result, search_safe_list, embed = await self.parse_link(ctx, request)
        #    if result is None or embed is None:
        #        return
#
        #view = QueueSelectedView(ctx, search_safe_list)
        #view.message = await ctx.send(view=view, embed=embed, content=f"{ctx.author.name} Requested {request}")
        #await view.wait()
#
        #return view.user_choice, search_safe_list
        #return search_safe_list
    
    def search_string(self, request: str, limit=4) -> list[SpotifyTrack]:
        if not "spotify.com/" in request:
            return self.spotify_service.perform_search(request, limit=limit)
        else:
            raise Exception("Unable to parse Spotify link. Please provide a query.")

    def parse_link(self, request: str) -> 'Union[SpotifyTrack, SpotifyPlaylist, SpotifyAlbum, SpotifyArtist, list[SpotifyTrack]]':
        """
        Handles Spotify link requests from the user.

        Args:
            ctx (commands.Context): The command context.
            self.spotify_service (SpotifyService): The Spotify service instance.
            request (str): The user's request.

        Returns:
            Optional[Union[SpotifyTrack, SpotifyPlaylist, SpotifyAlbum, SpotifyArtist, list[SpotifyTrack]]]: The search result and search queries.
        """
        if "show" in request or "episode" in request:
            #Throw exception
            raise Exception("Spotify Integration does not support shows or episodes. Please provide a link to a track, album, playlist, or artist.")
        
        try:
            result = None
            if "playlist" in request:
                result = self.spotify_service.get_playlist_by_id(request)
                #search_queries = [f"{item.track.name} - {item.track.artists[0].name}" for item in result.tracks.items]
                #embed = SpotifyEmbedCreator.create_playlist_embed(result)

            elif "track" in request:
                result = self.spotify_service.get_track_by_id(request)
                #search_queries = [f"{result.artists[0].name} - {result.name}"]
                #embed = SpotifyEmbedCreator.create_track_embed(result)

            elif "album" in request:
                result = self.spotify_service.get_album_by_id(request)
                #search_queries = [f"{item.name} - {item.artists[0].name}" for item in result.tracks.items]
                #embed = SpotifyEmbedCreator.create_album_embed(result)

            elif "artist" in request:
                artist = self.spotify_service.get_artist_by_id(request)
                result: list[SpotifyTrack] = self.spotify_service.get_artist_top_songs(artist.id)
                #search_queries = [f"{item.name} - {item.artists[0].name}" for item in result]
                #embed =  SpotifyEmbedCreator.create_artist_embed(artist, result)
            
            if result is None:
                raise Exception("No results found.")

            return result

        except Exception as e:
            print(f"An error occurred while handling the Spotify link: {e}")
            #await ctx.send(content="An error occurred while processing your request. Please try again later.")
            return None
        
    def _create_embed(self, result: 'Union[SpotifyTrack, SpotifyPlaylist, SpotifyAlbum, SpotifyArtist, list[SpotifyTrack]]'):
        embed = None
        if isinstance(result, list):
            embed = SpotifyEmbedCreator.create_playlist_embed(result)
        elif isinstance(result, SpotifyTrack):
            embed = SpotifyEmbedCreator.create_track_embed(result)
        elif isinstance(result, SpotifyPlaylist):
            embed = SpotifyEmbedCreator.create_playlist_embed(result)
        elif isinstance(result, SpotifyAlbum):
            embed = SpotifyEmbedCreator.create_album_embed(result)
        elif isinstance(result, SpotifyArtist):
            embed = SpotifyEmbedCreator.create_artist_embed(result)
        return embed
    
    def create_search_safe_list(self, result: 'Union[SpotifyTrack, SpotifyPlaylist, SpotifyAlbum, list[SpotifyTrack]]') -> list[str]:
        search_safe_list = None
        if isinstance(result, list):
            search_safe_list = [f"{item.name} - {item.artists[0].name}" for item in result]
        elif isinstance(result, SpotifyTrack):
            search_safe_list = [f"{result.artists[0].name} - {result.name}"]
        elif isinstance(result, SpotifyPlaylist):
            search_safe_list = [f"{item.track.name} - {item.track.artists[0].name}" for item in result.tracks.items]
        elif isinstance(result, SpotifyAlbum):
            search_safe_list = [f"{item.name} - {item.artists[0].name}" for item in result.tracks.items]
        
        if search_safe_list is None:
            raise Exception("No results found.")
        return search_safe_list