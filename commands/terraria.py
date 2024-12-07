import os

class Terraria(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="renew", help="Renews Terraria server")
    async def _renew(self, ctx, url: str):
        try:
            # First, call the renew_terraria_server function
            screenshot_path = await renew_terraria_server(url)
            
            # If a screenshot is returned, send it in Discord
            if screenshot_path:
                await ctx.send(f"Successfully renewed Terraria server on: **{url}**", file=discord.File(screenshot_path))
                
                # After sending the screenshot, delete the file
                os.remove(screenshot_path)
                print(f"Deleted screenshot at {screenshot_path}")
            else:
                await ctx.send(f"Successfully renewed Terraria server on: **{url}**, but no screenshot was taken.")
        except Exception as e:
            await ctx.send(e)

async def setup(bot):
    await bot.add_cog(Terraria(bot))
