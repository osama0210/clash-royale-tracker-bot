# Clash Royale Tracker Bot

A Discord bot that lets you look up Clash Royale stats using the official Clash Royale API.

> This project is no longer actively maintained.

## Commands

| Command | Description |
|---|---|
| `/player <tag>` | Look up a player's stats |
| `/clan <tag>` | Show clan information |
| `/compare <tag1> <tag2>` | Compare two players side by side |

## Installation

```bash
git clone https://github.com/osama0210/clash-royale-tracker-bot.git
cd clash-royale-tracker-bot

pip install -r requirements.txt
```

Create a `.env` file with your tokens:

```env
DISCORD_TOKEN=your_discord_token
CR_API_KEY=your_clash_royale_api_key
```

Then run:

```bash
python bot.py
```

## Built with

- [discord.py](https://discordpy.readthedocs.io/)
- [Clash Royale API](https://developer.clashroyale.com/)
