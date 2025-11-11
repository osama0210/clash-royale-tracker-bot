import discord
from discord.ext import commands
from services.clash_api import get_clan, norm_tag, ClashAPIError

def fmt_member(m):
    name = m.get("name", "—")
    cups = m.get("trophies", 0)
    role = m.get("role", "").replace("_", " ").title()
    return f"{name} — {cups} 🏆  ({role})"

class Clan(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.command(name="clan")
    async def clan_cmd(self, ctx, tag: str):
        try:
            data = await get_clan(tag)
        except ClashAPIError as e:
            return await ctx.reply(str(e))

        t = norm_tag(tag)
        name = data.get("name", "—")
        desc = data.get("description") or "—"
        badge = (data.get("badgeUrls") or {}).get("large")
        members = data.get("memberList", [])
        members_sorted = sorted(members, key=lambda x: x.get("trophies", 0), reverse=True)
        top5 = members_sorted[:5]

        e = discord.Embed(
            title=f"{name} (#{t})",
            description=desc[:300],  # kort houden
        )
        e.add_field(name="Trophies", value=str(data.get("clanScore", "—")), inline=True)
        e.add_field(name="Required", value=str(data.get("requiredTrophies", "—")), inline=True)
        e.add_field(name="Members", value=f"{data.get('members', 0)}/50", inline=True)
        e.add_field(name="Type", value=(data.get("type") or "—").title(), inline=True)
        e.add_field(name="Location", value=(data.get('location') or {}).get('name', '—'), inline=True)
        e.add_field(name="War Trophies", value=str(data.get("clanWarTrophies", "—")), inline=True)

        if top5:
            e.add_field(
                name="Top 5 leden",
                value="\n".join(fmt_member(m) for m in top5),
                inline=False
            )

        if badge: e.set_thumbnail(url=badge)
        await ctx.send(embed=e)

async def setup(bot):
    await bot.add_cog(Clan(bot))