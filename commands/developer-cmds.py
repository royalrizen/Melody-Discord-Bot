import discord
from discord.ext import commands, tasks
import yaml
import os
import config
from utils.staff import is_dev

class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = 'settings.yaml'
        self.allowed_servers = self.load_allowed_servers()
        self.check_servers.start()

    def load_allowed_servers(self):
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w') as f:
                yaml.dump([], f)
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f) or []

    def save_allowed_servers(self):
        with open(self.config_file, 'w') as f:
            yaml.dump(self.allowed_servers, f)

    @commands.command(name="allow_server", usage="<server id>", description="Allow the server to use this bot")
    @commands.check(is_dev)
    async def allow_server(self, ctx, server_id: int):
        if server_id not in self.allowed_servers:
            self.allowed_servers.append(server_id)
            self.save_allowed_servers()
            await ctx.send(f"{config.SUCCESS} Server `{server_id}` is now allowed to use Melody.")
        else:
            await ctx.send(f"{config.ERROR} Server `{server_id}` is already allowed.")

    @commands.command(name="unallow_server", usage="<server id>", description="Removes the server from whitelist")
    @commands.check(is_dev)
    async def unallow_server(self, ctx, server_id: int):
        if server_id in self.allowed_servers:
            self.allowed_servers.remove(server_id)
            self.save_allowed_servers()
            await ctx.send(f"{config.SUCCESS} Server `{server_id}` is now unallowed.")
        else:
            await ctx.send(f"{config.ERROR} Server `{server_id}` was not allowed.")

    @commands.command(name="servers", description="Servers the bot is in")
    @commands.check(is_dev)
    async def servers(self, ctx):
        embed = discord.Embed(title="Servers the bot is in")
        for guild in self.bot.guilds:
            invite = await guild.text_channels[0].create_invite(max_age=300)
            embed.add_field(name=guild.name, value=f"{guild.id} ([Invite]({invite.url}))", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="leave", description="Leaves all unallowed servers")
    @commands.check(is_dev)
    async def leave(self, ctx):
        for guild in self.bot.guilds:
            if guild.id not in self.allowed_servers:
                await guild.leave()
        await ctx.send("📤 Left all unallowed servers.")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if guild.id not in self.allowed_servers:
            await guild.leave()

    @tasks.loop(minutes=10)
    async def check_servers(self):
        for guild in self.bot.guilds:
            if guild.id not in self.allowed_servers:
                await guild.leave()

async def setup(bot):
    await bot.add_cog(Developer(bot))
