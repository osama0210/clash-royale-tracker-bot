import os
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
import discord

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Ingelogd als {bot.user}")


async def main():
    async with bot:
        await bot.load_extension("commands.player")
        await bot.load_extension("commands.clan")
        await bot.load_extension("commands.compare")
        await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())