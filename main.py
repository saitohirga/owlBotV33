import discord
import data.key
import datetime
from time import gmtime, strftime

bot = discord.Bot()


@bot.slash_command()
async def rat(ctx):
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

@bot.slash_command(name="userinfo", description="Gets info about a user.")
@discord.default_permissions(
    manage_messages=True,)
async def info(ctx: discord.ApplicationContext, user: discord.Member = None):
    user = (
        user or ctx.author
    )  # If no user is provided it'll use the author of the message
    embed = discord.Embed(
        fields=[
            discord.EmbedField(name="ID", value=str(user.id), inline=False),  # User ID
            discord.EmbedField(
                name="Created",
                value=discord.utils.format_dt(user.created_at, "F"),
                inline=False,
            ),  # When the user's account was created
        ],
    )
    embed.set_author(name=user.name)
    embed.set_thumbnail(url=user.display_avatar.url)

    if user.colour.value:  # If user has a role with a color
        embed.colour = user.colour

    if isinstance(user, discord.User):  # Checks if the user in the server
        embed.set_footer(text="This user is not in this server.")
    else:  # We end up here if the user is a discord.Member object
        embed.add_field(
            name="Joined",
            value=discord.utils.format_dt(user.joined_at, "F"),
            inline=False,
        )  # When the user joined the server

    await ctx.respond(embeds=[embed])  # Sends the embed

bot.run(data.key.token)
