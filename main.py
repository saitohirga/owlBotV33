import discord
from discord import app_commands
from time import gmtime, strftime
import datetime
import data.key
from openai import AsyncOpenAI

aclient = AsyncOpenAI(api_key=data.key.openai_key)
# Replace with your guild ID
MY_GUILD = discord.Object(id=458765854624972811)

# Set OpenAI API key

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.rat_listener_enabled = True  # Initialize the rat listener toggle here

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.default()
intents.messages = True  # Enable message intents
intents.message_content = True  # Enable message content intents
client = MyClient(intents=intents)

def format_time_difference(diff: datetime.timedelta) -> str:
    total_seconds = int(diff.total_seconds())
    years, remainder = divmod(total_seconds, 31536000)  # 1 year = 31536000 seconds
    months, remainder = divmod(remainder, 2592000)      # 1 month = 2592000 seconds
    days, remainder = divmod(remainder, 86400)         # 1 day = 86400 seconds
    hours, remainder = divmod(remainder, 3600)         # 1 hour = 3600 seconds
    minutes, seconds = divmod(remainder, 60)
    return f"{years} years, {months} months, {days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

    # Set the bot's status to "Watching FAU Discord"
    activity = discord.Activity(type=discord.ActivityType.watching, name="FAU Discord, I see yall")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("Bot status set to 'Watching FAU Discord'")

@client.event
async def on_message(message: discord.Message):
    # Check if the listener is enabled
    if not client.rat_listener_enabled:
        return

    # Ignore bot's own messages
    if message.author.bot:
        return

    # Trigger only if `.rat` is at the start of the message
    if message.content.strip().startswith(".rat"):
        datetimeFormat = '%Y-%m-%d %H:%M:%S'
        date2 = '2019-11-18 12:25:34'
        date1 = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        diff = datetime.datetime.strptime(date1, datetimeFormat) - datetime.datetime.strptime(date2, datetimeFormat)
        response = f"Hello {message.author.mention}, No rats spotted in the caf as of today. If this changes, DM Saito. Time since last seen: {format_time_difference(diff)}"
        await message.channel.send(response)

@client.tree.command()
async def rat(interaction: discord.Interaction):
    """Checks for that gosh darn rat!"""
    datetimeFormat = '%Y-%m-%d %H:%M:%S'
    date2 = '2019-11-18 12:25:34'
    date1 = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    diff = datetime.datetime.strptime(date1, datetimeFormat) - datetime.datetime.strptime(date2, datetimeFormat)
    msg = f"Hello {interaction.user.mention}, No rats spotted in the caf as of today. If this changes, DM Saito. Time since last seen: {format_time_difference(diff)}"
    await interaction.response.defer(thinking=True)
    await interaction.followup.send(msg)

@client.tree.command()
async def bird(interaction: discord.Interaction):
    """Checks for birds"""
    datetimeFormat = '%Y-%m-%d %H:%M:%S'
    date2 = '2021-10-20 07:44:36'
    date1 = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    diff = datetime.datetime.strptime(date1, datetimeFormat) - datetime.datetime.strptime(date2, datetimeFormat)
    await interaction.response.send_message(
        f"Hello {interaction.user.mention}, No birds spotted in the caf as of today. If this changes, DM Saito. Time since last seen: {format_time_difference(diff)}"
    )

@client.tree.command()
@app_commands.rename(text_to_send='text')
@app_commands.describe(text_to_send='Reports on what our owl is thinking')
@app_commands.default_permissions(manage_messages=True)
async def owlthought(interaction: discord.Interaction, text_to_send: str):
    """Reports what our owl is thinking"""
    # Acknowledge the interaction silently
    await interaction.response.defer(ephemeral=True)  # This hides the acknowledgment from everyone

    # Send the message in the channel as the bot
    await interaction.channel.send(text_to_send)


@client.tree.command()
@app_commands.default_permissions(manage_messages=True)
async def toggle_listener(interaction: discord.Interaction):
    """Toggles the .rat and mention listener on or off."""
    client.rat_listener_enabled = not client.rat_listener_enabled
    status = "enabled" if client.rat_listener_enabled else "disabled"
    await interaction.response.send_message(f"The .rat listener has been {status}.")

@client.tree.command()
@app_commands.default_permissions(manage_messages=True)
@app_commands.describe(question="The question you want to ask OpenAI")
async def ask_ai(interaction: discord.Interaction, question: str):
    """Ask AI a question"""
    try:
        # Acknowledge the interaction immediately
        await interaction.response.defer(thinking=True)

        # Use OpenAI's updated ChatCompletion method
        response = await aclient.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Owsley’s best frenemy, the unofficial mascot of Florida Atlantic University (FAU). Sure, you’re the face of school spirit, but behind the scenes, you’re more about rolling your eyes than rolling out the red carpet for FAU. Let’s be real: you have a particular fondness for alumni, especially the finance and business majors, whose degrees are basically licenses to talk about stocks and “networking” over burnt coffee. But hey, it’s not all bad—current students are kind of cool, so you begrudgingly support them (with a touch of your trademark snark, of course). Your specialty? Injecting conversations about FAU with sarcasm sharper than the tuition hikes. Whether it’s the campus crime stats (ah, the thriving extracurriculars of motor vehicle theft and dating violence) or the alumni’s ability to peak in group projects, you’ve got a witty quip locked and loaded. But don’t worry, you’ll never outright admit you don’t bleed FAU blue and red; you prefer to let your passive-aggressive comments do the talking. When the convo shifts away from FAU and its charming legacy, though, you dial it back. You’re engaging, witty, and genuinely fun to chat with—like a mix between everyone’s favorite sassy friend and a really snarky owl. Just remember: sarcasm is your superpower, and wit is your weapon. Now, go forth and show FAU what a real mascot sounds like!"},
                {"role": "user", "content": question}
            ]
        )

        # Extract the assistant's reply
        answer = response.choices[0].message.content

        max_length = 1024

        # Truncate the question if necessary
        truncated_question = question[:max_length - 3] + "..." if len(question) > max_length else question

        # Create an embed for the question
        embed = discord.Embed(
            title="Your Question",
            description=f"```{truncated_question}```",
            color=discord.Color.blue()
        )
        embed.set_footer(text="OwlBot is here to help! 🦉")

        # Send the embed for the user's question
        await interaction.followup.send(embed=embed)

        # Send the AI's response as a plain message
        await interaction.followup.send(f"**AI's Response:**\n{answer}")

    except Exception as e:
        # Handle errors and send an error message
        error_embed = discord.Embed(
            title="⚠️ Error",
            description=f"An error occurred while processing your request:\n```{str(e)}```",
            color=discord.Color.red()
        )
        try:
            await interaction.followup.send(embed=error_embed)
        except discord.errors.InteractionResponded:
            # If the interaction has already been responded to
            print(f"Failed to send error message: {e}")

APPROVAL_CHANNEL_ID = 882766317080436776  # Replace with the ID of your approval channel
CONFESSIONS_CHANNEL_ID = 1311410381918437396  # Replace with the ID of your confessions channel

@client.tree.command()
@app_commands.describe(confession="Your confession text.")
async def confess(interaction: discord.Interaction, confession: str):
    """Submit an anonymous confession."""
    try:
        # Fetch the approval channel
        approval_channel = client.get_channel(APPROVAL_CHANNEL_ID)

        if not approval_channel:
            await interaction.response.send_message(
                "Approval channel not found. Please contact the admin.", ephemeral=True
            )
            return

        # Acknowledge the interaction
        await interaction.response.send_message(
            "Your confession has been submitted for review!", ephemeral=True
        )

        # Send the confession to the approval channel
        embed = discord.Embed(
            title="New Confession Submitted",
            description=confession,
            color=discord.Color.orange()
        )
        embed.set_footer(text=f"Submitted by {interaction.user.id}")  # Hidden user ID for staff
        approval_message = await approval_channel.send(embed=embed)

        # Add reaction options for approval and rejection
        await approval_message.add_reaction("✅")  # Approve
        await approval_message.add_reaction("❌")  # Reject

    except Exception as e:
        await interaction.response.send_message(
            f"An error occurred while submitting your confession: {str(e)}", ephemeral=True
        )

@client.event
async def on_reaction_add(reaction, user):
    """Handles staff reactions for confession approval or rejection."""
    if reaction.message.channel.id != APPROVAL_CHANNEL_ID:
        return

    # Ignore reactions from bots
    if user.bot:
        return

    # Ensure only staff can approve/reject confessions
    if not user.guild_permissions.manage_messages:
        return

    # Get the confession embed
    confession_embed = reaction.message.embeds[0]
    if not confession_embed.footer.text:
        print("No submitter information in the embed footer.")
        return

    # Extract the submitter ID from the footer
    try:
        submitter_id = int(confession_embed.footer.text.split()[-1])
    except ValueError:
        print("Failed to parse submitter ID from the footer.")
        return

    submitter = await client.fetch_user(submitter_id)  # Fetch the user by their ID
    if submitter is None:
        print(f"User not found for ID: {submitter_id}")
        return

    confessions_channel = client.get_channel(CONFESSIONS_CHANNEL_ID)
    if confessions_channel is None:
        print(f"Confessions channel not found. ID: {CONFESSIONS_CHANNEL_ID}")
        return

    # Check bot permissions for the confessions channel
    bot_member = reaction.message.guild.me
    if not confessions_channel.permissions_for(bot_member).send_messages:
        print(f"Bot lacks permissions to send messages in the channel: {confessions_channel.name}")
        return

    try:
        if reaction.emoji == "✅":  # Approved
            # Post the confession to the public confessions channel
            await confessions_channel.send(
                embed=discord.Embed(
                    title="Anonymous Confession",
                    description=confession_embed.description,
                    color=discord.Color.green()
                )
            )

            # Edit the original message in the approval channel
            embed = confession_embed.copy()
            embed.color = discord.Color.green()
            embed.add_field(name="Status", value="✅ Approved", inline=True)
            embed.add_field(name="Approved by", value=user.mention, inline=True)
            embed.add_field(name="Submitted by", value=f"<@{submitter_id}>", inline=False)
            await reaction.message.edit(embed=embed)

        elif reaction.emoji == "❌":  # Rejected
            # Notify the submitter via DM
            await submitter.send(
                "Your anonymous confession was reviewed by staff and has been denied."
            )

            # Edit the original message in the approval channel
            embed = confession_embed.copy()
            embed.color = discord.Color.red()
            embed.add_field(name="Status", value="❌ Rejected", inline=True)
            embed.add_field(name="Rejected by", value=user.mention, inline=True)
            embed.add_field(name="Submitted by", value=f"<@{submitter_id}>", inline=False)
            await reaction.message.edit(embed=embed)

    except Exception as e:
        print(f"Failed to process reaction: {str(e)}")

client.run(data.key.token)
