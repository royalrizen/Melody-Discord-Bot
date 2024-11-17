import discord
from discord.ext import commands
from discord.ui import Button, View
import aiohttp
import random

class TruthDareRandomButton(discord.ui.View):

  def __init__(self, bot):
    super().__init__(timeout=None)
    self.bot = bot

  @discord.ui.button(label="Truth",
                     style=discord.ButtonStyle.green,
                     custom_id="truth")
  async def truth_button_callback(self, interaction: discord.Interaction,
                                  button: discord.ui.Button):
    await self._get_question(interaction, "truth")

  @discord.ui.button(label="Dare",
                     style=discord.ButtonStyle.red,
                     custom_id="dare")
  async def dare_button_callback(self, interaction: discord.Interaction,
                                 button: discord.ui.Button):
    await self._get_question(interaction, "dare")

  @discord.ui.button(label="Random",
                     style=discord.ButtonStyle.blurple,
                     custom_id="random")
  async def random_button_callback(self, interaction: discord.Interaction,
                                   button: discord.ui.Button):
    choice = random.choice(["truth", "dare"])
    await self._get_question(interaction, choice)

  async def _get_question(self, interaction, question_type, rating="pg"):
    async with aiohttp.ClientSession() as session:
      url = f"https://api.truthordarebot.xyz/v1/{question_type}?rating={rating}"
      async with session.get(url) as response:
        if response.status == 200:
          data = await response.json()
          embed = discord.Embed(title=data["question"],
                                color=discord.Color.blurple())
          embed.set_author(name=f"Requested by {interaction.user}",
                           icon_url=interaction.user.avatar.url)
          embed.set_footer(
              text=
              f"Type: {question_type.upper()} | Rating: {rating.upper()} | ID: {data['id']}"
          )
          await interaction.response.send_message(
              embed=embed, view=TruthDareRandomButton(self))
        else:
          await interaction.response.send_message("Failed to fetch question.")


class wyrButton(discord.ui.View):

  def __init__(self, bot):
    super().__init__(timeout=None)
    self.bot = bot

  @discord.ui.button(label="Would You Rather",
                     style=discord.ButtonStyle.blurple,
                     custom_id="wyr")
  async def wyr_button_callback(self, interaction: discord.Interaction,
                                button: discord.ui.Button):
    await self._get_wyr_question(interaction, "wyr")

  async def _get_wyr_question(self, interaction, question_type, rating="pg"):
    async with aiohttp.ClientSession() as session:
      url = f"https://api.truthordarebot.xyz/v1/{question_type}?rating={rating}"
      async with session.get(url) as response:
        if response.status == 200:
          data = await response.json()
          embed = discord.Embed(title=data["question"],
                                color=discord.Color.blurple())
          embed.set_author(name=f"Requested by {interaction.user}",
                           icon_url=interaction.user.avatar.url)
          embed.set_footer(
              text=
              f"Type: {question_type.upper()} | Rating: {rating.upper()} | ID: {data['id']}"
          )
          await interaction.response.send_message(embed=embed,
                                                  view=wyrButton(self))
        else:
          await interaction.response.send_message("Failed to fetch question.")


class nhieButton(discord.ui.View):

  def __init__(self, bot):
    super().__init__(timeout=None)
    self.bot = bot

  @discord.ui.button(label="Never Have I Ever",
                     style=discord.ButtonStyle.blurple,
                     custom_id="nhie")
  async def nhie_button_callback(self, interaction: discord.Interaction,
                                 button: discord.ui.Button):
    await self._get_nhie_question(interaction, "nhie")

  async def _get_nhie_question(self,
                               interaction,
                               question_type,
                               rating="pg"):
    async with aiohttp.ClientSession() as session:
      url = f"https://api.truthordarebot.xyz/v1/{question_type}?rating={rating}"
      async with session.get(url) as response:
        if response.status == 200:
          data = await response.json()
          embed = discord.Embed(title=data["question"],
                                color=discord.Color.blurple())
          embed.set_author(name=f"Requested by {interaction.user}",
                           icon_url=interaction.user.avatar.url)
          embed.set_footer(
              text=
              f"Type: {question_type.upper()} | Rating: {rating.upper()} | ID: {data['id']}"
          )
          await interaction.response.send_message(embed=embed,
                                                  view=nhieButton(self))
        else:
          await interaction.response.send_message("Failed to fetch question.")


class paranoiaButton(discord.ui.View):

  def __init__(self, bot):
    super().__init__(timeout=None)
    self.bot = bot

  @discord.ui.button(label="Paranoia",
                     style=discord.ButtonStyle.blurple,
                     custom_id="paranoia")
  async def paranoia_button_callback(self, interaction: discord.Interaction,
                                     button: discord.ui.Button):
    await self._get_paranoia_question(interaction, "paranoia")

  async def _get_paranoia_question(self,
                                   interaction,
                                   question_type,
                                   rating="pg"):
    async with aiohttp.ClientSession() as session:
      url = f"https://api.truthordarebot.xyz/v1/{question_type}?rating={rating}"
      async with session.get(url) as response:
        if response.status == 200:
          data = await response.json()
          embed = discord.Embed(title=data["question"],
                                color=discord.Color.blurple())
          embed.set_author(name=f"Requested by {interaction.user}",
                           icon_url=interaction.user.avatar.url)
          embed.set_footer(
              text=
              f"Type: {question_type.upper()} | Rating: {rating.upper()} | ID: {data['id']}"
          )
          await interaction.response.send_message(embed=embed,
                                                  view=paranoiaButton(self))
        else:
          await interaction.response.send_message("Failed to fetch question.")


class TruthDare(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    self.base_url = "https://api.truthordarebot.xyz/v1/"

  async def _get_question(self, ctx, question_type, rating="pg"):
    async with aiohttp.ClientSession() as session:
      url = f"{self.base_url}{question_type}?rating={rating}"
      async with session.get(url) as response:
        if response.status == 200:
          data = await response.json()
          embed = discord.Embed(title=data["question"],
                                color=discord.Color.blurple())
          embed.set_author(name=f"Requested by {ctx.author}",
                           icon_url=ctx.author.avatar.url)
          embed.set_footer(
              text=
              f"Type: {question_type.upper()} | Rating: {rating.upper()} | ID: {data['id']}"
          )
          await ctx.send(embed=embed, view=TruthDareRandomButton(self.bot))
        else:
          await ctx.send("Failed to fetch question.")

  async def _get_wyr_question(self, ctx, question_type, rating="pg"):
    async with aiohttp.ClientSession() as session:
      url = f"{self.base_url}{question_type}?rating={rating}"
      async with session.get(url) as response:
        if response.status == 200:
          data = await response.json()
          embed = discord.Embed(title=data["question"],
                                color=discord.Color.blurple())
          embed.set_author(name=f"Requested by {ctx.author}",
                           icon_url=ctx.author.avatar.url)
          embed.set_footer(
              text=
              f"Type: {question_type.upper()} | Rating: {rating.upper()} | ID: {data['id']}"
          )
          await ctx.send(embed=embed, view=wyrButton(self.bot))
        else:
          await ctx.send("Failed to fetch question.")

  async def _get_nhie_question(self, ctx, question_type, rating="pg"):
    async with aiohttp.ClientSession() as session:
      url = f"{self.base_url}{question_type}?rating={rating}"
      async with session.get(url) as response:
        if response.status == 200:
          data = await response.json()
          embed = discord.Embed(title=data["question"],
                                color=discord.Color.blurple())
          embed.set_author(name=f"Requested by {ctx.author}",
                           icon_url=ctx.author.avatar.url)
          embed.set_footer(
              text=
              f"Type: {question_type.upper()} | Rating: {rating.upper()} | ID: {data['id']}"
          )
          await ctx.send(embed=embed, view=nhieButton(self.bot))
        else:
          await ctx.send("Failed to fetch question.")

  async def _get_paranoia_question(self, ctx, question_type, rating="pg"):
    async with aiohttp.ClientSession() as session:
      url = f"{self.base_url}{question_type}?rating={rating}"
      async with session.get(url) as response:
        if response.status == 200:
          data = await response.json()
          embed = discord.Embed(title=data["question"],
                                color=discord.Color.blurple())
          embed.set_author(name=f"Requested by {ctx.author}",
                           icon_url=ctx.author.avatar.url)
          embed.set_footer(
              text=
              f"Type: {question_type.upper()} | Rating: {rating.upper()} | ID: {data['id']}"
          )
          await ctx.send(embed=embed, view=paranoiaButton(self.bot))
        else:
          await ctx.send("Failed to fetch question.")

  @commands.command()
  async def truth(self, ctx):
    await self._get_question(ctx, "truth")

  @commands.command()
  async def dare(self, ctx):
    await self._get_question(ctx, "dare")

  @commands.command()
  async def random(self, ctx):
    choice = random.choice(["truth", "dare"])
    await self._get_question(ctx, choice)

  @commands.command()
  async def wyr(self, ctx):
    await self._get_wyr_question(ctx, "wyr")

  @commands.command()
  async def nhie(self, ctx):
    await self._get_nhie_question(ctx, "nhie")

  @commands.command()
  async def paranoia(self, ctx):
    await self._get_paranoia_question(ctx, "paranoia")


async def setup(bot):
  await bot.add_cog(TruthDare(bot))
