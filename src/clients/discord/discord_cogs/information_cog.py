
import discord
from discord.ext import commands
from ..discord_audio.music_manager import MusicManager
from ..discord_integrations.youtube import YoutubeIntegration
from services.services_utils.service_factory import ServiceFactory
from ..discord_messages.discord_embed.services_embeds import YoutubeEmbedCreator, SpotifyEmbedCreator


from services.youtube.youtube_service import YouTube
from services.spotify.tracks import SpotifyTrack

class InfomationCog(commands.Cog):
    def __init__(self, bot, music_manager):
        self.bot = bot
        self.music_manager: 'MusicManager' = music_manager

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandError):
            if 'is not found' in str(error):
                return
            print(f'An error occurred in InformationCog: {str(error)}')

    @commands.command(name="info")
    async def info(self,ctx:commands.Context):
        if not self.music_manager.get_guild_voice_client(ctx.guild.id):
            await ctx.message.add_reaction("❌")
            await ctx.reply("I'm not in a voice channel right now.")
            return
        
        current_song = self.music_manager.get_current_song(ctx.guild.id)

        if not current_song:
            await ctx.message.add_reaction("❌")
            await ctx.reply("I'm not playing anything right now.")
            return
            
        await ctx.message.add_reaction("🔍")

        #Weird hacky fix. Getting the stream_url also gets the Youtube object.
        await current_song.get_stream_url()
        yt_info = current_song.yt_object
        embed = YoutubeEmbedCreator()
        embed = embed.create_video_embed(yt_info)

        await ctx.message.reply(embed=embed)

    @commands.command(name="queue")
    async def queue(self,ctx:commands.Context):
        if not self.music_manager.get_guild_voice_client(ctx.guild.id):
            await ctx.message.add_reaction("❌")
            await ctx.reply("I'm not in a voice channel right now.")
            return
        
        queue: list = self.music_manager.get_guild_queue(ctx.guild.id)
        if len(queue) > 0:
            await ctx.message.add_reaction("✅")
            message_to_send = await self.construct_queue_message(queue)
            await ctx.message.reply(f'Songs in queue: ``{len(queue)}``\nNext song(s):\n{message_to_send}')
            #await ctx.message.reply(f'This feature is still in development. There are currently `{len(queue)}` song(s) in queue.')
        else:
            await ctx.message.add_reaction("❌")
            await ctx.message.reply("There are no songs in the queue.")

    async def construct_queue_message(self, queue) -> str:
        message_parts = []
        for song in queue[:5]:
            await song.get_stream_url()
            
            yt_info = song.yt_object
            title = yt_info.title
            #channel_name = yt_info.channel_id
            url = yt_info.watch_url
            requester = song.ctx.author.display_name

            message_part = f"`{title}` - <{url}>\nRequested by: `{requester}`\n"
            message_parts.append(message_part)

        return "\n".join(message_parts)

async def setup(bot):
    mm = MusicManager(bot)
    await bot.add_cog(InfomationCog(bot, mm))