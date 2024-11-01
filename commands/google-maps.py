import discord
from discord.ext import commands
from playwright.async_api import async_playwright
import os
import traceback
import asyncio
from PIL import Image

class GoogleMaps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.browser = None 

    async def get_browser(self):
        if self.browser is None:
            async with async_playwright() as p:
                self.browser = await p.chromium.launch(headless=True)
        return self.browser

    @commands.command(name="map", aliases=["google_map", "maps", "gmap", "searchmap"], usage="<location>", description="Search any location on Google Maps")
    async def map(self, ctx, *, location: str):
        m1 = await ctx.send(f"🔎 *Searching for **'{location}'** on Google Maps...*")
        screenshot_path = "google_maps_screenshot.png"
        cropped_image_path = "cropped_image.png"

        try:
            location_url = location.replace(" ", "+")
            google_maps_url = f"https://google.com/maps/place/{location_url}"
            
            browser = await self.get_browser()
            page = await browser.new_page()

            await page.goto(google_maps_url, timeout=120000)
            await page.wait_for_load_state("networkidle")
            await ctx.send("*Loaded Google Maps for the specified location...*")
            
            await page.wait_for_selector("button[aria-label='Collapse side panel']", timeout=60000)
            await page.evaluate("document.querySelector('button[aria-label=\"Collapse side panel\"]').click()")
            await asyncio.sleep(2)
            
            await page.wait_for_selector("canvas", timeout=60000)
            await asyncio.sleep(2)
            
            map_element = await page.query_selector("canvas")
            if map_element:
                await map_element.screenshot(path=screenshot_path)              
                await ctx.send("*Taking screenshot...*")
            else:
                raise Exception("Map canvas not found.")

        except Exception as e:
            error_message = f"⚠️ {str(e)}"
            traceback_info = traceback.format_exc()

            if len(traceback_info) > 2000:
                for i in range(0, len(traceback_info), 2000):
                    await ctx.send(traceback_info[i:i + 2000])
            else:
                await ctx.send(error_message + "\n" + traceback_info)

        finally:
            # Crop the screenshot
            crop_white_space(screenshot_path, cropped_image_path)
            
            await m1.delete()            
            await ctx.send(file=discord.File(cropped_image_path))
            await page.close()  # Close the page but keep the browser open
            if os.path.exists(screenshot_path):
                os.remove(screenshot_path)
            if os.path.exists(cropped_image_path):
                os.remove(cropped_image_path)

def crop_white_space(image_path, output_path):
    image = Image.open(image_path)
    image = image.convert("RGBA")
    data = image.getdata()
    bbox = [image.width, image.height, 0, 0]

    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = data[y * image.width + x]
            if (r, g, b) != (255, 255, 255):
                if x < bbox[0]:
                    bbox[0] = x
                if y < bbox[1]:
                    bbox[1] = y
                if x > bbox[2]:
                    bbox[2] = x
                if y > bbox[3]:
                    bbox[3] = y

    cropped_image = image.crop((bbox[0], bbox[1], bbox[2] + 1, bbox[3] + 1))
    cropped_image.save(output_path)

async def setup(bot):
    await bot.add_cog(GoogleMaps(bot))
