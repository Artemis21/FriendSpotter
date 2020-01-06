from discord.ext import commands, tasks
from models.records import Records
from models.points import AllPoints
from main import analysis, drawing
import io
import discord


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ready = False

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.ready:
            Records.load(self.bot)
            AllPoints.load(self.bot)
            self.save.start()
            self.ready = True

    @tasks.loop(minutes=1)
    async def save(self):
        Records.save()
        AllPoints.save()

    def cog_unload(self):
        self.save()

    @commands.Cog.listener()
    async def on_message(self, message):
        Records.log(message)

    @commands.command(brief='Get a graph!')
    async def graph(self, ctx):
        points = analysis.analyse(ctx.guild)
        graph = drawing.Drawing(points)
        f = io.BytesIO()
        graph.image.save(f, format='PNG')
        f.seek(0)
        file = discord.File(f, 'network.png')
        await ctx.send(file=file)
    
