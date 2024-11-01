import discord
from discord.ext import commands
from playwright.async_api import async_playwright
import os
import asyncio
from PIL import Image

class GoogleMaps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="map", aliases=["google_map", "maps", "gmap", "searchmap"], usage="<location>", description="Search any location on Google Maps")
    async def map(self, ctx, *, location: str):
        m1 = await ctx.send(f"🔎 *Searching for **'{location}'** on Google Maps...*")
        screenshot_path = "google_maps_screenshot.png"
        cropped_image_path = "google_maps.png"

        try:
            location_url = location.replace(" ", "+")
            google_maps_url = f"https://google.com/maps/place/{location_url}"

            # Launch browser and open a new page
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
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
                    await ctx.send("⚠️ Map canvas not found.")
                
                # Close the page and browser automatically upon exit from async context

        finally:
            # Crop the screenshot
            crop_white_space(screenshot_path, cropped_image_path)
            
            await m1.delete()            
            await ctx.send(file=discord.File(cropped_image_path))

            # Clean up local files
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
