import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # laad .env bestand

TOKEN = os.getenv("DISCORD_TOKEN")
CLASH_API_KEY = os.getenv("CLASH_API_KEY")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
print("Token:", os.getenv("DISCORD_TOKEN"))
@bot.event
async def on_ready():
    print(f" Ingelogd als {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

bot.run(TOKEN)