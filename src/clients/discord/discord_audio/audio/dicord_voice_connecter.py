import discord
import asyncio

class DiscordVoiceConnecter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DiscordVoiceConnecter, cls).__new__(cls)
        return cls._instance

    async def connect_to_voice_channel(self, channel: discord.VoiceChannel) -> discord.VoiceClient:
        """
        Connect to the specified voice channel and return the VoiceClient object representing the connection.

        Parameters:
            channel (discord.VoiceChannel): The voice channel to connect to.

        Returns:
            discord.VoiceClient: A reference to the VoiceClient object representing the connection.
        """
        try:
            return await channel.connect()
        except discord.ClientException as e:
            print(f"Error connecting to voice channel: {e}")
        except Exception as e:
            print(f"Unknown error connecting to voice channel: {e}")
        return None
        
    async def disconnect_from_guild(self, voice_client: discord.VoiceClient) -> None:
        """
        Disconnect from the voice channel that the specified VoiceClient is connected to.

        Parameters:
            voice_client (discord.VoiceClient): The VoiceClient to disconnect from.

        Returns:
            None
        """
        async def disconnect():
            try:
                await voice_client.disconnect()
            except discord.ClientException as e:
                print(f"Error disconnecting from voice channel: {e}")
            except Exception as e:
                print(f"Unknown error disconnecting from voice channel: {e}")

        asyncio.create_task(disconnect())

    async def move_voice_client_to_voice_channel(self, voice_client: discord.VoiceClient, channel: discord.VoiceChannel) -> None:
        """
        Move the specified VoiceClient to the specified voice channel.

        Parameters:
            voice_client (discord.VoiceClient): The VoiceClient to move.
            channel (discord.VoiceChannel): The voice channel to move the VoiceClient to.
        
        Returns:
            None
        """
        async def move():
            try:
                await voice_client.move_to(channel)
            except discord.ClientException as e:
                print(f"Error moving voice client to channel: {e}")
            except Exception as e:
                print(f"Unknown error moving voice client to channel: {e}")

        asyncio.create_task(move())