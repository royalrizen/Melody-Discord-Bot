import discord
from discord.ext import commands
import aiohttp
import yaml 

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('settings.yaml', 'r') as file:
            settings = yaml.safe_load(file)
        self.settings = settings
        
        self.allowed_channel_id  = self.settings['channels']['memes']

    async def get_specific_meme(self, meme_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(meme_url) as response:
                data = await response.json()
                return data

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.lower() in ['meme pls', 'meme plz'] and message.channel.id == self.allowed_channel_id:
            meme_data = await self.get_specific_meme('https://meme-api.com/gimme')

            embed = discord.Embed()
            meme_url = meme_data['url']
            meme_title = meme_data['title']
            subreddit = meme_data['subreddit']
            embed.title = meme_title
            embed.url = meme_url
            embed.color = discord.Colour.random()
            embed.set_image(url=meme_url)
            embed.set_footer(text=f'r/{subreddit}')

            await message.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Memes(bot))
