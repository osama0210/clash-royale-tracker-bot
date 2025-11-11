import discord
from discord.ext import commands
from services.clash_api import get_player, norm_tag, ClashAPIError


class Compare(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="compare")  # <--- DIT HEB JE NODIG
    async def compare_cmd(self, ctx, tag1: str, tag2: str):
        await ctx.typing()

        try:
            p1 = await get_player(tag1)
            p2 = await get_player(tag2)
        except (ClashAPIError, ValueError) as e:
            return await ctx.reply(f"error: {e}")

        p1 = {
            "name": p1.get("name", "?"),
            "trophies": p1.get("trophies", 0),
            "best": p1.get("bestTrophies", 0),
            "level": p1.get("expLevel", 0)
        }

        p2 = {
            "name": p2.get("name", "?"),
            "trophies": p2.get("trophies", 0),
            "best": p2.get("bestTrophies", 0),
            "level": p2.get("expLevel", 0)
        }

        score1 = p1["trophies"] + p1["best"] + p1["level"]
        score2 = p2["trophies"] + p2["best"] + p2["level"]

        if score1 > score2:
            result = f"🏆 {p1['name']} is sterker dan {p2['name']}"
        elif score2 > score1:
            result = f"🏆 {p2['name']} is sterker dan {p1['name']}"
        else:
            result = f"🤝 {p1['name']} en {p2['name']} zijn even sterk!"

        embed = discord.Embed(
            title=f"{p1['name']} 🆚 {p2['name']}",
            description=result,
            color=discord.Color.gold()
        )

        embed.add_field(
            name="🏆 Trophies",
            value=f"{p1['trophies']} vs {p2['trophies']}  |  * {abs(p1['trophies'] - p2['trophies'])}",
            inline=False
        )

        embed.add_field(
            name="🥇 Best Trophies",
            value=f"{p1['best']} vs {p2['best']}  |  * {abs(p1['best'] - p2['best'])}",
            inline=False
        )

        embed.add_field(
            name="🔰 Level",
            value=f"{p1['level']} vs {p2['level']}  |  * {abs(p1['level'] - p2['level'])}",
            inline=False
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Compare(bot))
