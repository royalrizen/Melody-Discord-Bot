import discord
from discord.ext import commands
import asyncio
from playwright.async_api import async_playwright
import json
import os

class Terraria(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def load_cookies(self, context, cookies_file):
        with open(cookies_file, 'r') as file:
            cookies = json.load(file)
            await context.add_cookies(cookies)

    async def interact_with_site(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            await self.load_cookies(context, 'cookies.json')
            page = await context.new_page()
            await page.goto('https://panel.gaming4free.net')
            await page.goto('https://panel.gaming4free.net/server/d9d2619c/console')
            await page.wait_for_selector('button.VideoAd___StyledButton-sc-ye3fb7-0')
            await page.click('button.VideoAd___StyledButton-sc-ye3fb7-0')
            await asyncio.sleep(15)
            await browser.close()

    @commands.command(name="renew", description="Renews Terraria server")
    async def renew_server(self, ctx):
        await ctx.send("Starting server renewal process. Please wait...")
        try:
            self.create_cookies()
            await ctx.send("Cookies created!")
            await self.interact_with_site()
            await ctx.send("Server renewal process completed successfully!")
        except Exception as e:
            await ctx.send(e)

    def create_cookies(self):
        cookies_data = [
            {
                "name": "pterodactyl_session",
                "value": os.environ['PTERODACTYL_SESSION'],
                "domain": "panel.gaming4free.net",
                "path": "/",
                "httpOnly": True,
                "secure": True
            },
            {
                "name": "XSRF-TOKEN",
                "value": os.environ['XSRF_TOKEN'],
                "domain": "panel.gaming4free.net",
                "path": "/",
                "httpOnly": False,
                "secure": True
            },
            {
                "name": "_GRECAPTCHA",
                "value": os.environ['GRECAPTCHA_VALUE'],
                "domain": "panel.gaming4free.net",
                "path": "/",
                "httpOnly": False,
                "secure": True
            }
        ]
        with open("cookies.json", "w") as file:
            json.dump(cookies_data, file, indent=4)

async def setup(bot):
    await bot.add_cog(Terraria(bot))
