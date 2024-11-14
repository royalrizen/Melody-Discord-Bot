import discord
from discord.ext import commands, tasks
import yaml
import os

class Welcomer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = 'settings.yaml'
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = yaml.safe_load(f) or {}
        else:
            self.config = {"channels": {}}
            self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config, f)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_id = self.config["channels"].get("welcomer")
        if channel_id:
            channel = self.bot.get_channel(int(channel_id))
            if channel and channel.guild.id == member.guild.id:
                await self.send_welcome_embed(channel, member)

    async def send_welcome_embed(self, channel, member):
        display_name = member.display_name.replace(" ", "%20")
        avatar = member.avatar.url if member.avatar else member.default_avatar.url
        api = f"https://melodyyy.vercel.app/welcome?avatar={avatar}&username={member.name}&displayname={display_name}"
        embed = discord.Embed(
            title="Welcome! <a:blob_wave:1175022141599658054>",
            description="We are thrilled to have you in our community! Feel free to introduce yourself in <#1139591850567676104>.",
            color=0xffffff
        )
        embed.set_image(url=api)
        embed.set_footer(text=f"Account Created on {member.created_at.strftime('%d-%m-%Y')}")
        await channel.send(member.mention, embed=embed)

    @commands.command(name='set_welcome_channel', aliases=['swc'], usage="<channel>", description="Set the welcome channel for the server.")
    @commands.has_permissions(manage_guild=True)
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
        self.config["channels"]["welcomer"] = str(channel.id)
        self.save_config()
        await ctx.reply(f"Welcome channel set to {channel.mention}.", allowed_mentions=discord.AllowedMentions.none())

class MemberStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = 'settings.yaml'
        self.load_config()
        self.update_channel_name.start()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = yaml.safe_load(f) or {}
        else:
            self.config = {"channels": {}}
            self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config, f)

    @tasks.loop(minutes=10)
    async def update_channel_name(self):
        channel_id = self.config["channels"].get("memberstats")
        if channel_id:
            channel = self.bot.get_channel(int(channel_id))
            if channel:
                guild = channel.guild
                member_count = sum(1 for member in guild.members if not member.bot)
                await channel.edit(name=f'✦ {member_count} Members ✦')

    @update_channel_name.before_loop
    async def before_update_channel_name(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Welcomer(bot))
    await bot.add_cog(MemberStats(bot))
