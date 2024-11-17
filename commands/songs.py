import discord
from discord.ext import commands
from discord.ui import View 
import re
import yaml 
import config 

class Songs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistent_view = SongsView(bot)

    async def cog_load(self):
      self.bot.add_view(self.persistent_view)

    async def cog_unload(self):
      self.persistent_view.stop()

    @commands.command(name='songs', description="Sends the Share Songs embed")
    @commands.has_permissions(manage_guild=True)
    async def support(self, ctx):
        embed = discord.Embed(title="Share your favourite songs!", description="We want to hear the beats that make your heart skip! Click the button below and share the link to your favorite songs.\n\n( Spotify • Youtube • SoundCloud )")
        embed.set_image(url="https://i.ibb.co/Qmxmn1R/happy-music.gif")
        await ctx.message.delete()
        message = await ctx.send(embed=embed, view=SongsView(self.bot))

class SongsView(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        
    @discord.ui.button(label='Share', style=discord.ButtonStyle.blurple, emoji=config.SHARE, custom_id="sharebtn")
    async def share(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = SongsModal(self.bot)
        await interaction.response.send_modal(modal)
        
class SongsModal(discord.ui.Modal, title="Share your favourite songs!"):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        with open('settings.yaml', 'r') as file:
            settings = yaml.safe_load(file)
        self.settings = settings    
        self.songs_channel  = self.settings['channels']['songs']               
        self.song_link = discord.ui.TextInput(label='Link')
        self.add_item(self.song_link)

    async def on_submit(self, interaction: discord.Interaction):
        link = self.song_link.value

        if re.search(r'<@&\d+>', link):
            await interaction.response.send_message("Invalid link. It cannot contain role mentions. 😂", ephemeral=True)
            return
        
        if re.search(r'<@\d+>', link):
            await interaction.response.send_message("Invalid link. It cannot contain user mentions. 😂", ephemeral=True)
            return           

        if link.startswith("https://"):
            channel_id = self.songs_channel
            channel = self.bot.get_channel(channel_id)

            if "@here" in link or "@everyone" in link:
                await interaction.response.send_message("Lol you think you can ping everyone 😂", ephemeral=True)
            else:
                embed = discord.Embed(description=f"**╰➤ Shared by** {interaction.user.mention}", color=0xff0000) 

                message1 = await channel.send(link)
                message2 = await channel.send(embed=embed)
                await message2.add_reaction("♥️")
                await interaction.response.send_message(f"{config.SHARE} Shared!", ephemeral=True)
        else:
            await interaction.response.send_message('Invalid link format. Please provide a valid URL.', ephemeral=True)
        
async def setup(bot):
    await bot.add_cog(Songs(bot))
    
