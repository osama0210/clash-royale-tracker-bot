import discord # voor embeds, kleuren, berichten
from discord.ext import commands # Zorgt dat !compare werkt
from services.clash_api import get_player, norm_tag, ClashAPIError # haalt echte player data op van cr api
import json # om JSON bestanden uit te lezen binnen python
from datetime import datetime
import os # Checken of bestand bestaat

# een cog is een module in discord bots
class Compare(commands.Cog):
    # hier sla ik de bot in self.bot zodat deze class eraan gekoppeld is
    def __init__(self, bot):
        self.bot = bot

    # command definitie -> !compare
    @commands.command(name="compare")
    # ctx -> info van Discord welke kanaal bijvoorbeeld. ook geef ik de twee speler-tags mee
    async def compare_cmd(self, ctx, tag1: str, tag2: str):
        # hiermee zie je dat de bot aan het schrijven is
        await ctx.typing()

        try:
            # api request om de speler data terug te krijgen
            raw1 = await get_player(tag1)
            raw2 = await get_player(tag2)
        except (ClashAPIError, ValueError) as e:
            return await ctx.reply(f"error: {e}")

        # data noramliseren en opslaan in p1 en p2
        p1 = {
            "name": raw1.get("name", "?"),
            "trophies": raw1.get("trophies", 0), # als de data niet bestaat zet 0
            "best": raw1.get("bestTrophies", 0),
            "level": raw1.get("expLevel", 0)
        }

        p2 = {
            "name": raw2.get("name", "?"),
            "trophies": raw2.get("trophies", 0),
            "best": raw2.get("bestTrophies", 0),
            "level": raw2.get("expLevel", 0)
        }

        # een formule om te bepalen wie sterker is
        score1 = p1["trophies"] + p1["best"] + p1["level"]
        score2 = p2["trophies"] + p2["best"] + p2["level"]

        # spreekt voor zich
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
            value=f"{p1['trophies']} vs {p2['trophies']}  |  Δ {abs(p1['trophies'] - p2['trophies'])}",
            inline=False
        )

        embed.add_field(
            name="🥇 Best Trophies",
            value=f"{p1['best']} vs {p2['best']}  |  Δ {abs(p1['best'] - p2['best'])}",
            inline=False
        )

        embed.add_field(
            name="🔰 Level",
            value=f"{p1['level']} vs {p2['level']}  |  Δ {abs(p1['level'] - p2['level'])}",
            inline=False
        )

        # Hier toont Discord jouw kaart.
        await ctx.reply(embed=embed)

        self.save_compare_history(
            user=ctx.author.name,
            tag1=tag1,
            tag2=tag2,
            winner=p1['name'] if score1 > score2 else p2['name'] if score2 > score1 else "draw"
        )

    def save_compare_history(self, user, tag1, tag2, winner):
        path = "data/compare_history.json"

        if os.path.exists(path):
            with open(path, "r") as f:
                history = json.load(f)
        else:
            history = []

        entry = {
            "user": user,
            "tag1": tag1,
            "tag2": tag2,
            "winner": winner,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        history.append(entry)

        with open(path, "w") as f:
            json.dump(history, f, indent=4)


async def setup(bot):
    await bot.add_cog(Compare(bot))
