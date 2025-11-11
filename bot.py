# bot.py
import os, asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Ingelogd als {bot.user}")

async def main():
    async with bot:
        # Laad je commands hier
        await bot.load_extension("commands.player")
        # (later kun je ook clan/compare hier laden)
        await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())