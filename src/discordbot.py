import os
import argparse
from dotenv import load_dotenv
import discord
from discord.ext import commands
import traceback
import asyncio

def read_token(override_token=None):
    if override_token:
        return override_token
    load_dotenv()
    return os.getenv('DISCORD_BOT_TOKEN')

class DiscordBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def setup_hook(self):
        self.register_commands()

    def register_commands(self):
        pass

    async def on_ready(self):
        print(f"Logged in as {self.user.name}")

    async def on_message(self, message):
        if message.author != self.user:
            await self.process_commands(message)

    async def on_error(self, event, *args, **kwargs):
        error = traceback.format_exc()
        print(f'on_error: {error}')

# Entry point of the bot
async def main():
    parser = argparse.ArgumentParser(description="Discord bot")
    parser.add_argument('-o', '--override', type=str, help="Override token for the bot")
    args = parser.parse_args()

    override_token = args.override
    bot_token = read_token(override_token)

    if not bot_token:
        print("Error: No bot token provided. Use the environment variable or provide an override token with -o.")
        return

    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True

    bot = DiscordBot(command_prefix='!', intents=intents)
    await bot.load_extension('clients.discord.discord_cogs.play_cog')
    await bot.load_extension('clients.discord.discord_cogs.playback_cog')
    await bot.load_extension('clients.discord.discord_cogs.voicechannel_cog')
    await bot.load_extension('clients.discord.discord_cogs.information_cog')
    await bot.start(bot_token)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Bot shut down")
    except Exception as e:
        print(f"Error occurred in task: {e}")
