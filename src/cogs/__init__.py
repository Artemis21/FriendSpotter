from cogs.meta import Meta


def setup(bot):
    for i in (Meta,):
        bot.add_cog(i(bot))
