import discord
from discord.ext import commands
from time import gmtime, strftime
import datetime
from Utilities.Logging import autoLog


class Animals(commands.Cog):

    # attaches class of commands to existing client in main
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        autoLog('Animal cog online', 'okgreen')

    @commands.command()
    async def rat(self, ctx, name: str = None):
        print('called')
        """Checks for that gosh darn rat!"""
        name = name or ctx.author.name
        datetimeFormat = '%Y-%m-%d %H:%M:%S'
        date2 = '2019-11-18 12:25:34'
        date1 = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        diff = datetime.datetime.strptime(date1, datetimeFormat) - datetime.datetime.strptime(date2, datetimeFormat)
        await ctx.send(f"Hello {name}, No rats spotted in the caf as of today, if this changes DM Saito, time since " f"last seen {diff}")

def setup(client):
    client.add_cog(Animals(client))
