import discord
from discord.ext import commands
from playwright.async_api import async_playwright
import os
import traceback

class GoogleMaps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="map", aliases=["google_map", "maps", "gmap", "searchmap"], usage="<location>", description="Search any location on Google Maps")
    async def map(self, ctx, *, location: str):
        m = await ctx.send(f"🔎 *Searching for **'{location}'** on Google Maps...*")

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                await page.goto("https://www.google.com/maps", timeout=120000)
                await page.wait_for_load_state("networkidle")

                await page.wait_for_selector("#searchboxinput", timeout=60000)
                await page.fill("#searchboxinput", location)
                await page.press("#searchboxinput", "Enter")

                await page.wait_for_selector("canvas", timeout=60000)  # Wait for the map to load
                await page.wait_for_timeout(3000)  # Additional wait for the map to stabilize

                screenshot_path = "google_maps_screenshot.png"
                
                # Get the canvas element
                map_element = await page.query_selector("canvas")
                
                if map_element:
                    # Get bounding box of the canvas
                    bounding_box = await map_element.bounding_box()
                    if bounding_box:
                        # Take a screenshot of the canvas element
                        await map_element.screenshot(path=screenshot_path)
                    else:
                        raise Exception("Canvas bounding box could not be determined.")
                else:
                    raise Exception("Canvas element not found.")

                await browser.close()

            await m.delete()
            await ctx.send(file=discord.File(screenshot_path))
            os.remove(screenshot_path)
        except Exception as e:
            await m.delete()
            error_message = f"⚠️ {str(e)}"
            traceback_info = traceback.format_exc()

            if len(traceback_info) > 2000:
                for i in range(0, len(traceback_info), 2000):
                    await ctx.send(traceback_info[i:i + 2000])
            else:
                await ctx.send(error_message + "\n" + traceback_info)

async def setup(bot):
    await bot.add_cog(GoogleMaps(bot))
