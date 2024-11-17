import discord
from discord.ext import commands
from discord import app_commands as s
import asyncio

class StopwatchInstance:
    def __init__(self, bot, interaction):
        self.bot = bot
        self.interaction = interaction
        self.stopwatch_active = False
        self.elapsed_time = 0
        self.stopwatch_task = None
        self.message = None
        self.paused = False

    async def start(self):
        if self.stopwatch_active:
            await self.interaction.response.send_message("Stopwatch is already running!", ephemeral=True)
            return

        self.stopwatch_active = True
        self.paused = False
        self.elapsed_time = 0
        embed = discord.Embed(title="Stopwatch", description="## Loading...", color=0xffffff)
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1070823396834803732.png")
        await self.interaction.response.send_message(embed=embed)
        self.message = await self.interaction.original_response()

        self.stopwatch_task = self.bot.loop.create_task(self.update_stopwatch())

    async def update_stopwatch(self):
        """Updates the stopwatch every second."""
        while self.stopwatch_active:
            if not self.paused:
                await asyncio.sleep(1)
                self.elapsed_time += 1
                h, m, s = self.format_time(self.elapsed_time)
                embed = discord.Embed(title="Stopwatch", description=f"## **` {h:02} `:` {m:02} `:` {s:02} `**", color=discord.Color.green())
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1070823396834803732.png")
                await self.message.edit(embed=embed, view=StopwatchButton(self))
            else:
                await asyncio.sleep(1)

    async def pause(self):
        self.paused = True
        await self.message.edit(view=StopwatchButton(self))

    async def resume(self):
        self.paused = False
        await self.message.edit(view=StopwatchButton(self))

    async def stop(self):
        self.stopwatch_active = False
        if self.stopwatch_task:
            self.stopwatch_task.cancel()
            self.stopwatch_task = None

        h, m, s = self.format_time(self.elapsed_time)
        embed = discord.Embed(
            title="Stopwatch",
            description=f"## **` {h:02} `:` {m:02} `:` {s:02} `**",
            color=0xff0000
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1070823396834803732.png")
        await self.message.edit(embed=embed, view=StopwatchButton(self, disable_all=True))  # Disable all buttons

    def format_time(self, seconds):
        """Formats seconds into hours, minutes, and seconds."""
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return h, m, s


class Stopwatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stopwatches = {} 

    @s.command(name="stopwatch", description="Use the stopwatch to track time")
    @s.guild_only()
    async def start_stopwatch(self, interaction: discord.Interaction):
        stopwatch = StopwatchInstance(self.bot, interaction)
        self.stopwatches[interaction.user.id] = stopwatch
        await stopwatch.start()


class StopwatchButton(discord.ui.View):
    def __init__(self, stopwatch, disable_all=False):
        super().__init__(timeout=None)
        self.stopwatch = stopwatch

        self.pause_button.disabled = self.stopwatch.paused or disable_all
        self.resume_button.disabled = not self.stopwatch.paused or disable_all
        self.stop_button.disabled = disable_all

    @discord.ui.button(label="Pause", style=discord.ButtonStyle.secondary, row=1)
    async def pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.stopwatch.interaction.user.id:
            await interaction.response.send_message("You can't control this button!", ephemeral=True)
            return

        if not self.stopwatch.stopwatch_active:
            await interaction.response.send_message("Stopwatch is not running!", ephemeral=True)
            return

        await interaction.response.defer()
        await self.stopwatch.pause()

    @discord.ui.button(label="Resume", style=discord.ButtonStyle.primary, row=1)
    async def resume_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.stopwatch.interaction.user.id:
            await interaction.response.send_message("You can't control this button!", ephemeral=True)
            return

        if not self.stopwatch.stopwatch_active:
            await interaction.response.send_message("Stopwatch is not running!", ephemeral=True)
            return

        await interaction.response.defer()
        await self.stopwatch.resume()

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.danger, row=1)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.stopwatch.interaction.user.id:
            await interaction.response.send_message("You can't control this button!", ephemeral=True)
            return

        if not self.stopwatch.stopwatch_active:
            await interaction.response.send_message("Stopwatch is not running!", ephemeral=True)
            return

        await interaction.response.defer()
        await self.stopwatch.stop()

async def setup(bot):
    await bot.add_cog(Stopwatch(bot))
