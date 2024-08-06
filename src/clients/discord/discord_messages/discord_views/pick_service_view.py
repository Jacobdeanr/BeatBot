import discord
from discord.ext import commands

class PickServiceView(discord.ui.View):
    message: discord.Message | None = None
    """View that lets the user pick between YouTube and Spotify"""
    def __init__(self, ctx: commands.Context, query: str, youtube_service, spotify_service, timeout=3):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.query = query
        self.youtube_service = youtube_service
        self.spotify_service = spotify_service
        self.user_choice = None

    @discord.ui.button(label='YouTube', style=discord.ButtonStyle.red)
    async def youtube(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(thinking=False)
        self.user_choice = self.youtube_service
        await interaction.edit_original_response(view=discord.ui.View(), embed=None, content="One moment while I search YouTube...")
        await interaction.message.delete(delay=3)
        self.disable_buttons()
        self.stop()

    @discord.ui.button(label='Spotify', style=discord.ButtonStyle.green)
    async def spotify(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(thinking=False)
        self.user_choice = self.spotify_service
        await interaction.edit_original_response(view=discord.ui.View(), embed=None, content="One moment while I search Spotify...")
        await interaction.message.delete(delay=3)
        self.disable_buttons()
        self.stop()

    async def on_timeout(self):
        self.disable_buttons()
        await self.message.edit(view=discord.ui.View(), content="nothing was selected... I picked youtube for you.", embed=None)
        await self.message.delete(delay=3)
        self.disable_buttons()
        self.stop()

    #Utility functions
    def disable_buttons(self):
        for button in self.children:
            button.disabled = True