import discord
from discord.ext import commands
import config 
from utils.staff import is_staff

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="post", aliases=['send'], usage="-c <channel> -m <message>", description="Send a message through the bot")
    @commands.has_permissions(manage_guild=True)
    @commands.check(is_staff)
    async def _post(self, ctx, *, args=None):
        
        if args is None:
            await ctx.send("You need to provide a message!")
            return
        
        args = args.split(' ')
        channel = ctx.channel
        message = ""
        i = 0
        while i < len(args):
            if args[i] == '-c' and i + 1 < len(args):
                channel = discord.utils.get(ctx.guild.channels, mention=args[i + 1])
                i += 1
            elif args[i] == '-m' and i + 1 < len(args):
                message = ' '.join(args[i + 1:])
                break
            i += 1

        if not message:
            await ctx.send("You need to provide a message after -m!")
            return

        if not channel:
            await ctx.send("The specified channel was not found!")
            return
        
        await channel.send(message)

    @commands.command(name="avatar", aliases=["av"], usage="<optional_user>", description="Get a user's avatar")
    @commands.check(is_staff)
    async def avatar(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        av = user.avatar.url if user.avatar else user.default_avatar.url
        embed = discord.Embed(title=f"Avatar of **{user.name}**", color=0xcda69b)
        embed.set_image(url=av)
        await ctx.send(embed=embed)

    @commands.command(name="userinfo", aliases=["whois", "user"], usage="<user>", description="Fetch information about a user")
    @commands.check(is_staff)
    async def whois(self, ctx, member: discord.User = None):    
        if member is None:
            member = ctx.author 

        send_full_info = False
        created_at = f"<t:{int(member.created_at.timestamp())}:f>"

        if isinstance(member, discord.Member):
            send_full_info = True
            joined_at = f"<t:{int(member.joined_at.timestamp())}:f>"            
        
        user_info_embed = discord.Embed(color=config.PRIMARY_COLOR)

        default_pfp = member.avatar.url if member.avatar else member.default_avatar.url
        
        asset_fields = []
        if isinstance(member, discord.Member) and send_full_info:
            server_pfp = member.guild_avatar.url if member.guild_avatar else None
            banner = member.banner.url if member.banner else None

            if server_pfp:
                asset_fields.append(f"- [Server Profile Picture]({server_pfp})")
            if banner:
                asset_fields.append(f"- [Banner Picture]({banner})")

        asset_fields.append(f"- [Default Profile Picture]({default_pfp})")

        if send_full_info:            
            roles = sorted(member.roles[1:], key=lambda role: role.position, reverse=True)
            roles_display = ""
            if len(roles) > 10:
                roles_display = ", ".join(role.mention for role in roles[:10]) + f", ... ({len(roles) - 10} more)"
            else:
                roles_display = ", ".join(role.mention for role in roles)

            user_info_embed.description = (
                f"### Basic Information\n"
                f"** **\n"
                f"- Username: **`{member.name}`**\n"
                f"- Nickname: **`{member.display_name}`**\n"
                f"- Mention: {member.mention}\n"
                f"- User ID: **`{member.id}`**\n"
                f"- Created At: {created_at}\n"
                f"- Joined At: {joined_at}\n\n"
                f"### Roles\n"
                f"** **\n" +
                roles_display
            )
            if asset_fields:
                user_info_embed.description += "\n### Assets\n** **\n" + "\n".join(asset_fields)
        else:            
            user_info_embed.description = (
                f"### Basic Information\n"
                f"** **\n"
                f"- Username: **`{member.name}`**\n"
                f"- Nickname: **`{member.display_name}`**\n"
                f"- Mention: {member.mention}\n"
                f"- User ID: **`{member.id}`**\n"
                f"- Created At: {created_at}\n"
            )

            if asset_fields:
                user_info_embed.description += "\n### Assets\n** **\n" + "\n".join(asset_fields)

            user_info_embed.description += f"\n\n-# This user is not in the server."
            
        await ctx.send(embed=user_info_embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
