import discord_games as games
from discord_games import button_games
import discord
from discord.ext import commands

class Games(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    @commands.command(name="connect4", usage='<member>', description='Starts a game of connect4')
    async def connect4(self, ctx: commands.Context[commands.Bot], member: discord.User):
        game = games.ConnectFour(
            red=ctx.author,
            blue=member,
        )
        await game.start(ctx)

    @commands.command(name="hangman", description='Starts a game of hangman')
    async def hangman(self, ctx: commands.Context[commands.Bot]):
        game = games.Hangman()
        await game.start(ctx, delete_after_guess=True)

    @commands.command(name="chess", usage='<member>', description='Starts a game of chess')
    async def chess(self, ctx: commands.Context[commands.Bot], member: discord.User):

        game = games.Chess(
            white=ctx.author,
            black=member,
        )
        await game.start(ctx, timeout=60, add_reaction_after_move=True)

    @commands.command(name="typerace")
    async def typerace(self, ctx: commands.Context[commands.Bot]):

        game = games.TypeRacer()
        await game.start(ctx, timeout=30)

    @commands.command(name="battleship", usage='<member>', description='Starts a game of battleship, btw even I don\'t know how to play this game lmao')
    async def battleship(
        self, ctx: commands.Context[commands.Bot], member: discord.User
    ):

        game = games.BattleShip(ctx.author, member)
        await game.start(ctx)

    # Button Games: Requires discord.py >= v2.0.0

    @commands.command(name="tictactoe", usage='<member>', description='Starts a game of tictactoe')
    async def tictactoe(
        self, ctx: commands.Context[commands.Bot], member: discord.User
    ):
        game = button_games.BetaTictactoe(cross=ctx.author, circle=member)
        await game.start(ctx)

    @commands.command(name="wordle", description='Guess the word')
    async def wordle(self, ctx: commands.Context[commands.Bot]):

        game = button_games.BetaWordle()
        await game.start(ctx)

    @commands.command(name="akinator", aliases=['aki'], description='Play akinator on discord')
    async def guess(self, ctx: commands.Context[commands.Bot]):

        game = button_games.BetaAkinator()
        await game.start(ctx, timeout=120, delete_button=True)

    @commands.command(name="twenty48", description='Play the classic twenty48 game')
    async def twenty48(self, ctx: commands.Context[commands.Bot]):

        game = button_games.BetaTwenty48(render_image=True)
        await game.start(ctx)

    @commands.command(name="memory", description='Let\'s see how sharp your memory is')
    async def memory_game(self, ctx: commands.Context[commands.Bot]):

        game = button_games.MemoryGame()
        await game.start(ctx)

    @commands.command(name="rps", description='Play the classic rock paper scissor')
    async def rps(
        self, ctx: commands.Context[commands.Bot], player: discord.User = None
    ):

        game = button_games.BetaRockPaperScissors(
            player
        )
        await game.start(ctx)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Games(bot))
