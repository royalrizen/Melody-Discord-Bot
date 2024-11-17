import discord
from discord.ext import commands
from discord.ui import View 
import yaml 
import config

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistent_view = SupportView()

    async def cog_load(self):
      self.bot.add_view(self.persistent_view)

    async def cog_unload(self):
      self.persistent_view.stop()

    @commands.command(name='support', description="Sends the support embed")
    @commands.has_permissions(manage_guild=True)
    async def support(self, ctx):
        embed = discord.Embed(description=f"## {config.STAFF}  TICKET SUPPORT\n** **\nWe can provide assistance with:\n\n- **Reporting a server member**\n  - Please provide [user ID](https://dis.gd/findmyid) along with evidence.\n  - Our jurisdiction is limited to this server only.\n- **Partnerships**\n  - Please read <#1202211935110828093> before opening a ticket for this.\n- **Server Inquiries**\n\n-# Trolling in tickets will lead to punishments.")
        await ctx.message.delete()
        message = await ctx.send(embed=embed, view=SupportView())

class SupportView(View):
    def __init__(self):
        super().__init__(timeout=None)
        with open('settings.yaml', 'r') as file:
            settings = yaml.safe_load(file)
        self.settings = settings        
        self.support_channel  = self.settings['channels']['support']                              
    @discord.ui.button(label='Create a Ticket', style=discord.ButtonStyle.gray, emoji=config.TICKET, custom_id="ticketbtn")
    async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        channel_id = self.support_channel
        channel = interaction.guild.get_channel(channel_id) if interaction.guild else None
        if channel:
            await interaction.response.send_message('Creating ticket...', ephemeral=True)
            msg = await channel.send(f"$new {user_id} Support")
            await msg.delete(delay=3)
        else:
            print('Error: Guild not found [Support View]')
            
async def setup(bot):
    await bot.add_cog(Support(bot))
