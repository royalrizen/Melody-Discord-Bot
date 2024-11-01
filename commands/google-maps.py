import discord
from discord.ext import commands
from playwright.async_api import async_playwright
import os
import traceback
import asyncio

class GoogleMaps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="map", aliases=["google_map", "maps", "gmap", "searchmap"], usage="<location>", description="Search any location on Google Maps")
    async def map(self, ctx, *, location: str):
        m1 = await ctx.send(f"🔎 *Searching for **'{location}'** on Google Maps...*")
        screenshot_path = "google_maps_screenshot.png"

        try:
            location_url = location.replace(" ", "+")
            google_maps_url = f"https://google.com/maps/place/{location_url}"
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                await page.goto(google_maps_url, timeout=120000)
                await page.wait_for_load_state("networkidle")
                await ctx.send("*Loaded Google Maps for the specified location...*")
                
                await page.wait_for_selector("canvas", timeout=60000)

                await page.evaluate("""() => {
                    const collapseButton = document.querySelector('[aria-label="Collapse side panel"]');
                    if (collapseButton) {
                        collapseButton.click();
                    }
                }""")
                
                await asyncio.sleep(5)
                
                map_element = await page.query_selector("canvas")
                if map_element:
                    await map_element.screenshot(path=screenshot_path)              
                    await ctx.send("*Taking screenshot...*")
                else:
                    raise Exception("Map canvas not found.")

                await browser.close()
            
            await m1.delete()            
            await ctx.send(file=discord.File(screenshot_path))
        
        except Exception as e:
            error_message = f"⚠️ {str(e)}"
            traceback_info = traceback.format_exc()

            if len(traceback_info) > 2000:
                for i in range(0, len(traceback_info), 2000):
                    await ctx.send(traceback_info[i:i + 2000])
            else:
                await ctx.send(error_message + "\n" + traceback_info)

        finally:
            if os.path.exists(screenshot_path):
                os.remove(screenshot_path)

async def setup(bot):
    await bot.add_cog(GoogleMaps(bot))
