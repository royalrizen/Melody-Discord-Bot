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
        screenshot_path = "google_maps_screenshot.png"
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                # Load Google Maps and wait for network to be idle
                await page.goto("https://www.google.com/maps", timeout=120000)
                await page.wait_for_load_state("networkidle")

                # Fill the search box with the location and press Enter
                await page.wait_for_selector("#searchboxinput", timeout=60000)
                await page.fill("#searchboxinput", location)
                await page.press("#searchboxinput", "Enter")

                # Wait for the map canvas to load and stabilize
                await page.wait_for_selector("canvas", timeout=60000)
                await page.wait_for_timeout(3000)

                # Take a screenshot of the map area
                map_element = await page.query_selector("canvas")
                if map_element:
                    await map_element.screenshot(path=screenshot_path)
                else:
                    raise Exception("Map canvas not found.")

                await browser.close()
            
            await m.delete()
            await ctx.send(file=discord.File(screenshot_path))
        
        except Exception as e:
            await m.delete()
            error_message = f"⚠️ {str(e)}"
            traceback_info = traceback.format_exc()

            # Send error messages in chunks if too long
            if len(traceback_info) > 2000:
                for i in range(0, len(traceback_info), 2000):
                    await ctx.send(traceback_info[i:i + 2000])
            else:
                await ctx.send(error_message + "\n" + traceback_info)

        finally:
            # Cleanup screenshot file if it exists
            if os.path.exists(screenshot_path):
                os.remove(screenshot_path)

async def setup(bot):
    await bot.add_cog(GoogleMaps(bot))
