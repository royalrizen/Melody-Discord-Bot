import discord
from discord.ext import commands
from playwright.async_api import async_playwright
import os

class GoogleMaps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="map", aliases=["google_map", "maps", "gmap", "searchmap"], usage="<location>", description="Search any location on Google Maps")
    async def map(self, ctx, *, location: str):
        m = await ctx.send(f"🔎 *Searching for **'{location}'** on Google Maps...*")

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            await page.goto("https://www.google.com/maps")
            await page.fill("input[aria-label='Search Google Maps']", location)
            await page.press("input[aria-label='Search Google Maps']", "Enter")

            await page.wait_for_load_state("networkidle")

            screenshot_path = "google_maps_screenshot.png"  # Change the path if needed
            await page.screenshot(path=screenshot_path, full_page=True)
            await browser.close()

        await m.delete()
        await ctx.send(file=discord.File(screenshot_path))
        os.remove(screenshot_path)

async def setup(bot):
    await bot.add_cog(GoogleMaps(bot))
