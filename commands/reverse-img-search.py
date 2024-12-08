import discord
from discord import app_commands
from discord.ext import commands
import requests
import os

class ReverseImageSearch(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name='Reverse Image Search',
            callback=self.reverse_search,
        )
        self.bot.tree.add_command(self.ctx_menu)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

    async def reverse_search(self, interaction: discord.Interaction, message: discord.Message) -> None:
        if not message.attachments:
            await interaction.response.send_message("The message doesn't contain any attachments.", ephemeral=True)
            return

        attachment = message.attachments[0]
        if not attachment.filename.lower().endswith(('jpg', 'jpeg', 'png')):
            await interaction.response.send_message("Not a valid image file (JPG, JPEG, PNG).", ephemeral=True)
            return

        try:
            # Perform reverse image search using the provided API
            result = self.perform_reverse_search(attachment.url)

            if result:
                await interaction.response.send_message(f"Reverse Image Search Results:\n```\n{result}\n```")
            else:
                await interaction.response.send_message("No results found for the reverse image search.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred during reverse search: {e}", ephemeral=True)

    def perform_reverse_search(self, image_url):
        """Upload the image URL to the reverse image search API."""
        try:
            url = "https://google-reverse-image-api.vercel.app/reverse"
            data = {"imageUrl": image_url}
            response = requests.post(url, json=data)

            if response.ok:
                return response.json()
            else:
                return f"Error: Received status code {response.status_code}"
        except Exception as e:
            return f"Error during reverse search: {e}"

async def setup(bot):
    await bot.add_cog(ReverseImageSearch(bot))
