# services/clash_api.py
import os, re, aiohttp, asyncio
from dotenv import load_dotenv
load_dotenv()

BASE = os.getenv("CR_BASE_URL", "https://api.clashroyale.com/v1")
TOKEN = os.getenv("CR_API_TOKEN") or os.getenv("CLASH_API_KEY")
TAG_RE = re.compile(r"^[0289PYLQGRJCUV]+$")

class ClashAPIError(Exception): pass

def norm_tag(raw: str) -> str:
    t = raw.replace("#","").strip().upper()
    if not TAG_RE.fullmatch(t): raise ClashAPIError("❌ Ongeldige tag.")
    return t

async def _get(path: str):
    if not TOKEN: raise ClashAPIError("❌ CR_API_TOKEN ontbreekt.")
    async with aiohttp.ClientSession() as s:
        async with s.get(f"{BASE}{path}", headers={"Authorization": f"Bearer {TOKEN}"}, timeout=8) as r:
            if r.status in (401,403): raise ClashAPIError("❌ Authorization/IP fout (401/403).")
            if r.status == 429:       raise ClashAPIError("⏳ Rate limit, probeer zo weer (429).")
            if r.status == 404:       raise ClashAPIError("❌ Niet gevonden (404).")
            if r.status >= 400:       raise ClashAPIError(f"❌ API error {r.status}.")
            return await r.json()

async def get_player(tag: str):
    tag = norm_tag(tag)
    return await _get(f"/players/%23{tag}")

async def get_clan(tag: str):
    tag = norm_tag(tag)
    return await _get(f"/clans/%23{tag}")