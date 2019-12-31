from cogs.meta import Meta
from cogs.main import Main


def setup(bot):
    for i in (Main, Meta):
        bot.add_cog(i(bot))
