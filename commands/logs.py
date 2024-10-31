import discord
from discord.ext import commands
import yaml
import time
import config

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot        
        with open('settings.yaml', 'r') as file:
            settings = yaml.safe_load(file)
        self.settings = settings

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        message_logs_channel_id = self.settings['log_channels']['message_logs']
        message_logs_channel = self.bot.get_channel(message_logs_channel_id)

        if message_logs_channel:
            timestamp = int(time.time())
            message_url = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"

            embed = discord.Embed(description=f"**🗑️ [MESSAGE DELETED]({message_url})**", color=config.PRIMARY_COLOR)

            embed.add_field(
                name=f"in #{message.channel.name} ({message.channel.id})", 
                value=f"by {message.author.mention} at <t:{timestamp}:t>", 
                inline=False
            )

            if message.content:
                if len(message.content) > 1014:
                    message.content = message.content[:1011] + "..."
                    
                embed.add_field(
                    name="Message",
                    value=f"```\n{message.content}\n```",
                    inline=False
                )

            if message.attachments:
                attachment_links = "\n".join([attachment.url for attachment in message.attachments])
                embed.add_field(
                    name=f"Attachments [{len(message.attachments)}]",
                    value=attachment_links,
                    inline=False
                )

            if message.reference and isinstance(message.reference.resolved, discord.Message):
                replied_to = message.reference.resolved
                replied_to_url = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{replied_to.id}"
                embed.add_field(
                    name="Replied to",
                    value=replied_to_url,
                    inline=False
                )

            embed.set_footer(text=f"{message.author.name} • {message.author.id}", icon_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)

            await message_logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return

        message_logs_channel_id = self.settings['log_channels']['message_logs']
        message_logs_channel = self.bot.get_channel(message_logs_channel_id)

        if message_logs_channel:
            timestamp = int(time.time())
            message_url = f"https://discord.com/channels/{before.guild.id}/{before.channel.id}/{before.id}"

            embed = discord.Embed(description=f"**📝 [MESSAGE EDITED]({message_url})**", color=config.SECONDARY_COLOR)

            embed.add_field(
                name=f"in #{before.channel.name} ({before.channel.id})", 
                value=f"by {before.author.mention} at <t:{timestamp}:t>", 
                inline=False
            )

            if before.content or after.content:
                if len(before.content) > 1014:
                    before.content = before.content[:1011] + "..."

                if len(after.content) > 1014:
                    after.content = after.content[:1011] + "..."

                embed.add_field(
                    name="Before",
                    value=f"```\n{before.content}\n```",
                    inline=False
                )

                embed.add_field(
                    name="After",
                    value=f"```\n{after.content}\n```",
                    inline=False
                )

            embed.set_footer(text=f"{before.author.name} • {before.author.id}", icon_url=before.author.avatar.url if before.author.avatar else before.author.default_avatar.url)

            await message_logs_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Logging(bot))
