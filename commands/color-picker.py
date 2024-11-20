import discord
from discord.ext import commands
import requests
import re
import os

class ColorPicker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def rgb_to_hex(rgb):
        """Convert an RGB tuple to a HEX string."""
        return f'{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

    @staticmethod
    def parse_color_input(color_input):
        """Parse the color input and determine if it's HEX or RGB."""
        hex_pattern = re.compile(r'^#?([A-Fa-f0-9]{6})$')
        rgb_pattern = re.compile(r'^(\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})$')

        hex_match = hex_pattern.match(color_input)
        rgb_match = rgb_pattern.match(color_input)

        if hex_match:
            return hex_match.group(1).upper()
        elif rgb_match:
            rgb = tuple(map(int, rgb_match.groups()))
            if all(0 <= val <= 255 for val in rgb):
                return ColorPicker.rgb_to_hex(rgb).upper()
        return None

    @commands.command()
    async def color(self, ctx, *, color_input: str):
        """Command to display color information."""
        hex_code = self.parse_color_input(color_input)
        if not hex_code:
            await ctx.send("Invalid color format! Use HEX (e.g., `#123456`) or RGB (e.g., `255, 255, 255`).")
            return

        api_url = f"https://www.thecolorapi.com/id?format=svg&named=false&hex={hex_code}"
        response = requests.get(api_url)

        if response.status_code == 200:
            svg_path = f"{hex_code}.svg"
            with open(svg_path, "wb") as file:
                file.write(response.content)

            png_path = f"{hex_code}.png"
            os.system(f"rsvg-convert -o {png_path} {svg_path}")

            embed = discord.Embed(
                title=f"Color: #{hex_code}",
                description="Here is the color you selected:",
                color=int(hex_code, 16)
            )
            embed.set_image(url=f"attachment://{png_path}")
            await ctx.send(embed=embed, file=discord.File(png_path))

            os.remove(svg_path)
            os.remove(png_path)
        else:
            await ctx.send("Failed to fetch color information. Please try again later.")

async def setup(bot):
    await bot.add_cog(ColorPicker(bot))
