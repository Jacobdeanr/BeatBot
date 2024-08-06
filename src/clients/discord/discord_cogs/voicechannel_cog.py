import discord
from discord.ext import commands

from ..discord_audio.music_manager import MusicManager

class VoicechannelCog(commands.Cog):
    def __init__(self, bot, music_manager):
        self.bot = bot
        self.music_manager: 'MusicManager' = music_manager

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandError):
            if 'is not found' in str(error):
                return
            print(f'An error occurred in VoicechannelCog: {str(error)}')

    @commands.command(name="join")
    async def join(self, ctx: commands.Context):
        if ctx.author.voice is None:
            await ctx.message.add_reaction("❌")
            await ctx.reply("You must be in a voice channel to use this command.")
            return
        
        response = await self.music_manager.join_voice_channel(ctx.guild.id, ctx.message.author.voice.channel.id)
        if response:
            await ctx.message.add_reaction("👋")
        else:
            await ctx.message.add_reaction("❌")

    @commands.command(name="disconnect")
    async def disconnect(self, ctx: commands.Context):
        if ctx.author.voice is None:
            await ctx.message.add_reaction("❌")
            await ctx.reply("You must be in a voice channel to use this command.")
            return
        
        if not self.music_manager.get_guild_voice_client(ctx.guild.id):
            await ctx.message.add_reaction("❌")
            await ctx.reply("I'm not in a voice channel right now.")
            return
        
        if ctx.author.voice.channel.id != self.music_manager.get_guild_voice_client(ctx.guild.id).channel.id:
            await ctx.message.add_reaction("❌")
            await ctx.reply("You must be in the same voice channel as the bot to use this command.")
            return
        
        response = await self.music_manager.disconnect_from_guild(ctx.guild.id) 
        if response:
            await ctx.message.add_reaction("😢")
        else:
            await ctx.message.add_reaction("❌")

async def setup(bot):
    mm = MusicManager(bot)
    await bot.add_cog(VoicechannelCog(bot, mm))
