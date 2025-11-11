# commands/compare.py
import discord
from discord.ext import commands
from services.clash_api import get_player, norm_tag, ClashAPIError


class Compare(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="compare")
    async def compare_cmd(self, ctx, tag1: str, tag2: str):
        await ctx.typing()
        try:
            p1 = await get_player(tag1)
            p2 = await get_player(tag2)
        except (ClashAPIError, ValueError) as e:
            return await ctx.reply(f"❌ {e}")

        await ctx.reply(f"OK: {p1.get('name', '?')} vs {p2.get('name', '?')}")


async def setup(bot):
    await bot.add_cog(Compare(bot))