from ..discord_messages.discord_views.four_button_view import FourButtonView
from discord.ext import commands
import random

#sinlgeton
class SharedIntegration:
    def __init__(self):
        pass
    
    @staticmethod
    async def handle_search_results(ctx: commands.Context, results: list, create_embed_func):
        """
        Handles the search results by displaying them to the user and allowing them to select an option.

        Args:
            ctx (commands.Context): The command context.
            results (list): The list of search results.
            create_embed_func (callable): The function to create the embed for the search results.

        Returns:
            list: The selected result or None if no result was selected.
        """
        searchview = FourButtonView(timeout=5)
        interaction_embed = create_embed_func(results)

        searchview.message = await ctx.send(content="This is what I found", view=searchview, embed=interaction_embed)

        await searchview.wait()

        if searchview.choice is None:
            searchview.choice = random.randint(0, len(results) - 1)

        return results[searchview.choice]