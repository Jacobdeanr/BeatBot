from typing import Union
import discord
from discord.ext import commands

from services.services_utils.service_factory import ServiceFactory
from services.youtube.youtube_service import YouTubeService
from services.spotify.spotify_service import SpotifyService

from ..discord_audio.music_manager import MusicManager
from ..discord_messages.discord_views.pick_service_view import PickServiceView

from ..discord_integrations.spotify import SpotifyIntegration
from ..discord_integrations.youtube import YoutubeIntegration

from ..discord_audio.queue.queue_item import QueueItem

class PlayCog(commands.Cog):
    def __init__(self, bot, music_manager):
        self.bot: discord.Client = bot
        self.music_manager: MusicManager = music_manager

    #Entry point    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandError):
            if 'is not found' in str(error):
                return
            print(f'An error occurred in PlayCog: {str(error)}')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Check if the member is not the bot itself
        if member.id != self.bot.user.id:
            # Check every voice client (in case the bot is connected to multiple guilds)
            for vc in self.bot.voice_clients:
                if vc.guild == member.guild:
                    # Ensure the voice client is connected to a channel
                    if vc.channel:
                        # Count members in the voice channel, excluding bots
                        non_bot_members = len([m for m in vc.channel.members if not m.bot])
                        
                        # If no non-bot members are left in the channel, disconnect
                        if non_bot_members == 0:
                            await self.music_manager.disconnect_from_guild(member.guild.id)

    @commands.command(name="play")
    async def play(self, ctx: commands.Context, *, query: str):
        if ctx.author.voice is None:
            await ctx.message.add_reaction("❌")
            await ctx.reply("You must be in a voice channel to use this command.")
            return
        
        if not query:
            await ctx.message.add_reaction("❌")
            await ctx.reply("Please provide a search query.")
            return

        query = query.strip()
        
        items_to_queue, media_object = await self._handle_request(ctx, query)
        
        for item in items_to_queue:
            queue_item = QueueItem(item, ctx)
            self.music_manager.add_item_to_queue(ctx.guild.id, queue_item)

        await self.music_manager.play_queue_in_channel(ctx.guild.id, ctx.author.voice.channel.id)
        
        await ctx.message.add_reaction("✅")

    async def _handle_generic_request(self, ctx: commands.Context, query) -> 'Union[YouTubeService, SpotifyService]':
        yt = ServiceFactory().get_service("www.youtube.com")
        sp = ServiceFactory().get_service("www.spotify.com")

        embed = discord.Embed(title="Pick a service", description=f"\nPlease pick a service to search on. Default search will be YouTube if nothing is selected.", color=0x228b22)
        
        view = PickServiceView(timeout=5, ctx=ctx, query=query, youtube_service=yt, spotify_service=sp)
        view.message = await ctx.send(view=view, embed=embed)
        
        await view.wait()  # Wait until the user makes a choice or the view times out
        
        #No choice, default to YouTube
        if view.user_choice is None:
            return yt
        
               
        return view.user_choice
    
    async def _handle_request(self, ctx: commands.Context, query):
        """
        Handle a request for audio playback.

        Args:
            ctx (commands.Context): The context of the command.
            query (str): The query for the audio playback.

        Returns:
            None

        Raises:
            Exception: If there is an error handling the generic request or parsing the link.
        """
        service_integration: 'Union[YoutubeIntegration, SpotifyIntegration]' | None = ServiceFactory().get_service(query)
        
        if service_integration is None:
            try:
                #This request wasn't a link. Prompt the user to pick a service.
                service_integration = await self._handle_generic_request(ctx, query)
                media_object = service_integration.search_string(query, limit=1)[0]
            except Exception as e:
                print(f"Failed to handle generic request: {e}")
                return
        else:
            try:
                media_object = self._parse_link(service_integration, query)
            except Exception as e:
                print(f"Failed to parse link: {e}")
                return

        try:
            search_items = self._deconstruct_media_to_list(media_object, service_integration)
        except Exception as e:
            print(f"Failed to create queue search items: {e}")
        
        if search_items:
            return search_items, media_object

    def _deconstruct_media_to_list(self, media_object, integration: 'Union[YoutubeIntegration, SpotifyIntegration]') -> list:
        """
        Creates a single data type from the given media object and integration.

        Args:
            media_object: The media object to create the data type from.
            integration: The integration to use for creating the data type.

        Returns:
            A list of search items created from the media object.

        Raises:
            Exception: If the search items cannot be created.
        """
        search_items = None 
        try:
            search_items: list = integration.create_search_safe_list(media_object)
        except Exception as e:
            print(f"Failed to create search items: {e}")
            return
            
        if search_items is None:
            raise Exception("Failed to create search items")
        
        return search_items

    def _parse_link(self, service_integration: 'Union[YoutubeIntegration, SpotifyIntegration]', web_link: str):
        """
        Parses a link using the provided service and query.

        Parameters:
            service_integration (Union[YoutubeIntegration, SpotifyIntegration]): The audio service to use.
            web_link (str): The link to be parsed.

        Returns:
            A parsed media object or a list of media objects, depending on the query.
        """
        try:
            response = service_integration.parse_link(web_link)
            return response
        except Exception as e:
            print(f"Error: {e}")

    async def _build_user_interaction(self, ctx, query) -> tuple:
        audio_service = ServiceFactory().get_service(query)
        try:    
            if audio_service is None:
                audio_service = await self._handle_generic_request(ctx, query)

            #HACK: This is a temporary fix for the fact that the user isn't selecting any service.
            if audio_service == 'fast':
                yt = YoutubeIntegration(ServiceFactory().get_service('youtube'))
                choice, list_to_queue = await yt.handle_request(ctx, query, True)

            if isinstance(audio_service, SpotifyService):
                sp = SpotifyIntegration(audio_service)
                choice, list_to_queue = await sp.handle_request(ctx, query)

            elif isinstance(audio_service, YouTubeService):
                yt = YoutubeIntegration(audio_service)
                choice, list_to_queue = await yt.handle_request(ctx, query, False)

            if choice is None:
                return None, None
            if list_to_queue is None:
                return None, None
            
            return choice, list_to_queue
        except Exception as e:
            print(f"Error in _build_user_interaction: {e}")
            return None, None

    def _handle_queue_choice(self, guild_id, choice, list_to_queue) -> bool:
        if choice is None:
            return False
        
        if choice == 'cancel':
            return False
        
        if choice == 'add_to_queue':
            self._add_list_to_queue(guild_id, list_to_queue)

        elif choice == 'play_next':
            self._add_list_to_queue(guild_id, reversed(list_to_queue), 0)
        return True

    def _add_list_to_queue(self, guild_id, list_to_queue:list) -> None:
        for item in list_to_queue:
            self.music_manager.add_item_to_queue(guild_id, item)



async def setup(bot):
    mm = MusicManager(bot)
    await bot.add_cog(PlayCog(bot, mm))