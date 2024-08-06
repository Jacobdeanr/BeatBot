
import discord
from discord.ext import commands
from ..discord_audio.music_manager import MusicManager

class PlaybackCog(commands.Cog):
    def __init__(self, bot, music_manager):
        self.bot = bot
        self.music_manager: 'MusicManager' = music_manager

    #Entry point    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandError):
            if 'is not found' in str(error):
                return
            print(f'An error occurred in PlaybackCog: {str(error)}')
        
    @commands.command(name="pause")
    async def pause(self, ctx: commands.Context):
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
        
        response: bool = self.music_manager.pause_playback(ctx.guild.id)
        if response:
            await ctx.message.add_reaction("⏸️")
        else:
            await ctx.message.add_reaction("❌")
            await ctx.reply("Hey, I'm already paused ok?")

    @commands.command(name="resume")
    async def resume(self, ctx: commands.Context):
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
        
        response: bool = self.music_manager.resume_playback(ctx.guild.id)
        if response:
            await ctx.message.add_reaction("▶️")
        else:
            await ctx.message.add_reaction("❌")
            await ctx.reply("Sorry, I'm not paused right now.")

    @commands.command(name="skip")
    async def skip(self, ctx: commands.Context):
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
        
        response = self.music_manager.skip_playback(ctx.guild.id)
        if response:
            await ctx.message.add_reaction("⏭️")
        else:
            await ctx.message.add_reaction("❌")

    @commands.command(name="clear")
    async def clear(self, ctx: commands.Context):
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
        
        response = self.music_manager.clear_queue(ctx.guild.id)
        if response is True:
            await ctx.message.add_reaction("✅")
        else:
            await ctx.message.add_reaction("❌")
            await ctx.reply("The queue is already empty.")


async def setup(bot):
    mm = MusicManager(bot)
    await bot.add_cog(PlaybackCog(bot, mm))