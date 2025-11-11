# commands/player.py
import discord
from discord.ext import commands
from services.clash_api import get_player, norm_tag, ClashAPIError

class Player(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.command(name="player")
    async def player_cmd(self, ctx, tag: str):
        try:
            data = await get_player(tag)
        except (ClashAPIError, ValueError) as e:
            return await ctx.reply(str(e))

        t = norm_tag(tag)
        e = discord.Embed(title=f"{data['name']} (#{t})")
        e.add_field(name="Trophies", value=str(data.get("trophies","—")), inline=True)
        e.add_field(name="Best",     value=str(data.get("bestTrophies","—")), inline=True)
        e.add_field(name="Level",    value=str(data.get("expLevel","—")), inline=True)
        clan = data.get("clan")
        if clan:
            e.add_field(name="Clan", value=f"{clan['name']} ({clan['tag']})", inline=False)
        fav = (data.get("currentFavouriteCard") or {}).get("name", "—")
        e.add_field(name="Fav card", value=fav, inline=True)
        badge = (data.get("badges") or [{}])[0].get("iconUrls", {}).get("large")
        if badge: e.set_thumbnail(url=badge)
        await ctx.send(embed=e)

async def setup(bot):
    await bot.add_cog(Player(bot))