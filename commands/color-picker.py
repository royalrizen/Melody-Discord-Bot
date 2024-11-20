import discord
from discord.ext import commands
import requests

class Color(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="color")
    async def color_(self, ctx, color: str):
        if color.startswith("rgb(") and color.endswith(")"):
            rgb_values = color[4:-1].split(",")
            try:
                r, g, b = int(rgb_values[0].strip()), int(rgb_values[1].strip()), int(rgb_values[2].strip())
                hex_color = f"{r:02x}{g:02x}{b:02x}"
            except ValueError:
                await ctx.send("Invalid RGB format. Please use rgb(R, G, B) where R, G, and B are integers.")
                return
        elif color.startswith("#"):
            hex_color = color.lstrip("#")
        else:
            hex_color = color.lower()

        url = f"https://www.thecolorapi.com/id?hex={hex_color}"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            image_url = data['image']['bare']

            embed = discord.Embed(title=f"Color: {color.capitalize()}", description=f"Here is the image for the color {color.capitalize()}.", color=discord.Color(int(hex_color, 16)))
            embed.set_image(url=image_url)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Sorry, I couldn't find an image for the color {color}.")

async def setup(bot):
    await bot.add_cog(Color(bot))
