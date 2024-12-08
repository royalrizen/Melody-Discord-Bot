# extract exif data from images 
import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image
from PIL.ExifTags import TAGS
import os

class Exif(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name='Exif',
            callback=self.exif,
        )
        self.bot.tree.add_command(self.ctx_menu)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

    async def exif(self, interaction: discord.Interaction, message: discord.Message) -> None:
        if not message.attachments:
            await interaction.response.send_message("The message doesn't contain any attachments.", ephemeral=True)
            return

        attachment = message.attachments[0]
        if not attachment.filename.lower().endswith(('jpg', 'jpeg', 'png', 'tiff')):
            await interaction.response.send_message("Not a valid image file (JPG, JPEG, PNG, TIFF).", ephemeral=True)
            return

        file_path = f"./temp_{attachment.filename}"
        await attachment.save(file_path)

        exif_data = self.get_exif_data(file_path)
        os.remove(file_path)

        if exif_data:
            await interaction.response.send_message(f"EXIF Data:\n```\n{exif_data}\n```")
        else:
            await interaction.response.send_message("No EXIF data found or an error occurred.", ephemeral=True)

    def get_exif_data(self, image_path):
        """Extract EXIF data from the given image."""
        try:
            image = Image.open(image_path)
            exif_data = image._getexif()
            if not exif_data:
                return None

            exif = {TAGS.get(tag, tag): value for tag, value in exif_data.items()}
            return "\n".join(f"{key}: {value}" for key, value in exif.items())
        except Exception as e:
            return f"Error extracting EXIF data: {e}"

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Exif(bot))
