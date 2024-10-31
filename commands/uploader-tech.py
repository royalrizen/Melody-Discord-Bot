import discord
from discord.ext import commands
import requests
import config 
from utils.staff import is_dev

# https://uploader.tech/

class Uploader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.upload_api_key = config.UPLOADER_TECH_API_KEY

    @commands.command(name="upload", usage="<attach image>", description="Image hosting with custom domain.")
    @commands.check(is_dev)
    async def upload(self, ctx):
        if not ctx.message.attachments:
            await ctx.send("Please attach an image to upload.")
            return

        attachment = ctx.message.attachments[0]
        image_data = await attachment.read()
        url = "https://uploader.tech/api/upload"
        headers = {"key": self.upload_api_key}
        files = {"file": (attachment.filename, image_data)}
        response = requests.post(url, headers=headers, files=files)

        if response.status_code == 200:
            json_response = response.json()
            uploaded_image_url = json_response.get('url')
            await ctx.send(f"Image uploaded successfully: {uploaded_image_url}")
        else:
            json_response = response.json()
            error_message = json_response.get('message', 'An error occurred while uploading the image.')
            await ctx.send(f"Failed to upload image: {error_message}")

async def setup(bot):
    await bot.add_cog(Uploader(bot))
