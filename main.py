import discord
import data.key
import datetime
from time import gmtime, strftime

bot = discord.Bot()


@bot.slash_command()
async def rat(ctx, name: str = None):
    """Checks for that gosh darn rat!"""
    name = name or ctx.author.name
    datetimeFormat = '%Y-%m-%d %H:%M:%S'
    date2 = '2019-11-18 12:25:34'
    date1 = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    diff = datetime.datetime.strptime(date1, datetimeFormat) - datetime.datetime.strptime(date2, datetimeFormat)
    await ctx.respond(f"Hello {name}, No rats spotted in the caf as of today, if this changes DM Saito, time since "
                      f"last seen {diff}")


# @bot.user_command(name="Say Hello")
# async def hi(ctx, user):
#    await ctx.respond(f"{ctx.author.mention} says hello to {user.name}!")


bot.run(data.key.token)
