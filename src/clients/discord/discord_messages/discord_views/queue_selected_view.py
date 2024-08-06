import discord
from discord.ext import commands
import traceback
import typing

class QueueSelectedView(discord.ui.View):
    message: discord.Message | None = None
    def __init__(self, ctx: commands.Context, result):
        super().__init__(timeout=5)
        self.ctx = ctx
        self.user_choice = 'add_to_queue'  # To capture the user's choice

    async def on_timeout(self):
        self.disable_buttons()
        self.user_choice = 'add_to_queue'
        if self.message is not None:
            await self.message.edit(content="Nothing Selected. Added to Queue.", view=self, embed=None) 
            await self.message.delete(delay=3)
            self.stop()

    def disable_buttons(self):
        for button in self.children:
            button.disabled = True

    async def on_error(
        self, interaction: discord.Interaction[discord.Client], error: Exception, item: discord.ui.Item[typing.Any]
    ) -> None:
        tb = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        message = f"An error occurred while processing the interaction for {str(item)}:\n```py\n{tb}\n```"
        await interaction.response.send_message(message)


    @discord.ui.button(label='Add to Queue', style=discord.ButtonStyle.green)
    async def add_album(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.disable_buttons()
        self.user_choice = 'add_to_queue'
        await interaction.response.edit_message(content="Added to Queue", view=self, embed=None)
        await self.message.delete(delay=3)
        self.stop()

    @discord.ui.button(label='Play Next', style=discord.ButtonStyle.green)
    async def add_song(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.disable_buttons() 
        self.user_choice = 'play_next'
        await interaction.response.edit_message(content="Playing Next", view=self, embed=None)
        await self.message.delete(delay=3)
        self.stop()
        
    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.disable_buttons()
        self.user_choice = 'cancel'
        await interaction.response.edit_message(content="Canceled", view=self, embed=None)
        await self.message.delete(delay=3)
        self.stop()