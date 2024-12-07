import discord
from discord.ext import commands
from utils.terrariarenew import renew_terraria_server

class Terraria(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="renew", help="Renews Terraria server")
    async def _renew(self, ctx, url: str):
        try:
            await renew_terraria_server(url)
            await ctx.send(f"Successfully renewed Terraria server on: **{url}**")
        except Exception as e:
            await ctx.send(e)

async def setup(bot):
    await bot.add_cog(Terraria(bot))
