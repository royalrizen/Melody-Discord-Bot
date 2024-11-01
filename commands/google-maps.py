import discord
from discord.ext import commands
from playwright.async_api import async_playwright
import os
import asyncio
from PIL import Image
import config

class GoogleMaps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.browser = None  # Browser will be initialized in setup_browser

    async def setup_browser(self):
        if not self.browser:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=True)
    
    async def close_browser(self):
        if self.browser:
            await self.browser.close()
            await self.playwright.stop()
            self.browser = None

    @commands.command(name="map", aliases=["google_map", "maps", "gmap", "searchmap"], usage="<location>", description="Search any location on Google Maps")
    async def map(self, ctx, *, location: str):
        screenshot_path = "google_maps.png"
        cropped_image_path = "google_maps_screenshot.png"

        await self.setup_browser()  # Ensure the browser is ready

        try:
            await ctx.message.add_reaction(config.GOOGLE_SEARCH)

            location_url = location.replace(" ", "+")
            google_maps_url = f"https://google.com/maps/place/{location_url}"
            
            page = await self.browser.new_page()
            await page.goto(google_maps_url, timeout=120000)
            await page.wait_for_load_state("networkidle")
            
            retry_count = 3
            for attempt in range(retry_count):
                try:
                    await page.wait_for_selector("canvas", timeout=20000)
                    map_element = await page.query_selector("canvas")
                    if map_element:
                        await map_element.screenshot(path=screenshot_path)
                        break
                except Exception as e:
                    if attempt < retry_count - 1:
                        await asyncio.sleep(2)
                    else:
                        await ctx.send(f"{config.ERROR} Unable to capture the map screenshot.")
                        return
            await page.close()

            crop_white_space(screenshot_path, cropped_image_path)

            embed = discord.Embed(title="Google Maps", description=f"Location: **`{location}`**", color=discord.Color.blue())
            file = discord.File(cropped_image_path, filename="map.png")
            embed.set_image(url="attachment://map.png")
            await ctx.send(embed=embed, file=file)
        
        except Exception as e:
            print(f"Error: {e}")

        finally:
            await ctx.message.clear_reactions()
            await async_remove_files([screenshot_path, cropped_image_path])

    def cog_unload(self):
        asyncio.create_task(self.close_browser())

def crop_white_space(image_path, output_path):
    image = Image.open(image_path).convert("RGBA")
    bbox = image.getbbox()
    if bbox:
        cropped_image = image.crop(bbox)
        cropped_image.save(output_path)

async def async_remove_files(paths):
    for path in paths:
        if os.path.exists(path):
            try:
                await asyncio.to_thread(os.remove, path)
            except Exception as e:
                print(f"Error removing file {path}: {e}")

async def setup(bot):
    await bot.add_cog(GoogleMaps(bot))
    await cog.setup_browser()
