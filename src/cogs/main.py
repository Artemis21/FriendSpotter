from discord.ext import commands, tasks
from models.records import Records


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ready = False

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.ready:
            Records.load(self.bot)
            self.save.start()
            self.ready = True

    @tasks.loop(minutes=1)
    async def save(self):
        Records.save()

    def cog_unload(self):
        Records.save()

    @commands.Cog.listener()
    async def on_message(self, message):
        Records.log(message)
