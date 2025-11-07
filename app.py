import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # Needed to read messages
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Set your channel IDs here
SOURCE_CHANNEL_ID = "MAIN CHANNEL ID HERE (without the quotes)"  # Channel to listen for messages
DESTINATION_CHANNEL_ID = "TAD SYNC CHANNEL ID HERE (without the quotes)"  # Channel to send new messages

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id != SOURCE_CHANNEL_ID:
        return

    text_to_check = message.content or ""

    # If the message has embeds, extract their text too
    if message.embeds:
        for embed in message.embeds:
            if embed.title:
                text_to_check += f"\n{embed.title}"
            if embed.description:
                text_to_check += f"\n{embed.description}"
            for field in embed.fields:
                text_to_check += f"\n{field.name}: {field.value}"

    # Now check for "Boosted"
    if "Boosted" in text_to_check and "Stump" not in text_to_check:
        parts = text_to_check.split("Boosted:", 1)
        if len(parts) > 1:
            content_after = parts[1].strip()
            content_after = content_after.replace(" ", "")  # Remove spaces
            follow_to_message = f"FollowTo {content_after}"

            dest_channel = bot.get_channel(DESTINATION_CHANNEL_ID)
            if dest_channel:
                await dest_channel.send(follow_to_message)
            else:
                print("Destination channel not found.")

# ⚠️ Replace with your new bot token (regenerate if leaked!)
bot.run("BOT TOKEN HERE")
