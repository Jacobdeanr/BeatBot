import discord
from discord.ext import commands

class FourButtonView(discord.ui.View):
    message: discord.Message | None = None
    def __init__(self, timeout):
        super().__init__(timeout=timeout)
        self.choice = None

    def disable_buttons(self):
        for button in self.children:
            button.disabled = True

    async def on_timeout(self):
        await self.message.delete()
        self.disable_buttons()
        self.stop()

    @discord.ui.button(label='Result 1', style=discord.ButtonStyle.primary)
    async def result_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.disable_buttons() 
        self.choice = 0
        await interaction.message.delete()
        self.stop()

    @discord.ui.button(label='Result 2', style=discord.ButtonStyle.primary)
    async def result_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.disable_buttons()
        self.choice = 1
        await interaction.message.delete()
        self.stop()
        
    @discord.ui.button(label='Result 3', style=discord.ButtonStyle.primary)
    async def result_3(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.disable_buttons()
        self.choice = 2
        await interaction.message.delete()
        self.stop()

    @discord.ui.button(label='Result 4', style=discord.ButtonStyle.primary)
    async def result_4(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.disable_buttons()
        self.choice = 3
        await interaction.message.delete()
        self.stop()