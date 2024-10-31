import discord
from discord.ext import commands
from playwright.async_api import async_playwright
import os
import asyncio 

class Screenshot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="screenshot", aliases=["ss"], usage="<url>", description="Take screenshot of a website.")
    @commands.has_permissions(administrator=True)
    async def screenshot(self, ctx, url: str):
        m = await ctx.send('📸 **`Taking screenshot...`**')
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)
            
            # Wait for the page to finish loading
            await page.wait_for_load_state('networkidle')  # Wait until network is idle

            screenshot_path = f'screenshot_{ctx.message.id}.png'
            await page.screenshot(path=screenshot_path)
            await browser.close()
            await m.delete()

            await ctx.send(file=discord.File(screenshot_path))
            os.remove(screenshot_path)

async def setup(bot):
    await bot.add_cog(Screenshot(bot))
