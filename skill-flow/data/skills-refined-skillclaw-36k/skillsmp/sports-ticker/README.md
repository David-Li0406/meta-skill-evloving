# 🏆 Sports Ticker

**Live sports alerts with scoring updates and real-time stats — completely FREE!**

Track soccer, football, basketball, hockey, baseball, F1, and more!

Built for [Clawdbot](https://clawdbot.com) but works standalone too.

## ✨ Features

- 🎯 **Multi-sport support** — Soccer, NFL, NBA, NHL, MLB, F1, and more!
- ⚽ **Live scoring alerts** with player names and times
- 🟥 **Key events** — cards, touchdowns, home runs, goals
- ⏸️ **Period updates** — Halftime, quarters, intermissions
- 🏁 **Final results** with WIN/LOSS/DRAW
- 📊 **Multi-team support** — track as many teams as you want
- 🔄 **Auto-scheduling** — cron jobs for match days (Clawdbot)
- 💰 **100% FREE** — no API keys, no subscriptions!

## 🎯 The Secret Sauce: ESPN API

This skill uses ESPN's public API which provides:
- Real-time scores across multiple sports
- Scoring plays with player names and timestamps
- Game events (touchdowns, goals, home runs, etc.)
- Match/game statistics

**No API key required!** ESPN's API is open and free to use.

### Supported Sports & Leagues

**⚽ Soccer/Football**
- Premier League (`eng.1`), La Liga (`esp.1`), Bundesliga (`ger.1`), Serie A (`ita.1`)
- Champions League (`uefa.champions`), Europa League (`uefa.europa`)
- MLS (`usa.1`), Liga MX (`mex.1`), and 20+ more

**🏈 American Football**
- NFL (`nfl`)

**🏀 Basketball**
- NBA (`nba`), WNBA (`wnba`), NCAA (`mens-college-basketball`)

**🏒 Hockey**
- NHL (`nhl`)

**⚾ Baseball**
- MLB (`mlb`)

**🏎️ Racing**
- Formula 1 (`f1`)

## 🚀 Quick Start

### 1. Install

```bash
# Clone or copy to your skills directory
clawdhub install sports-ticker

# Or manually
git clone https://github.com/your-repo/sports-ticker
cd sports-ticker
```

### 2. Configure Your Teams

```bash
# Interactive setup
python3 scripts/setup.py

# Or find team IDs directly
python3 scripts/setup.py find "Lakers" basketball
python3 scripts/setup.py find "Chiefs" football
python3 scripts/setup.py find "Barcelona" soccer
```

Common team IDs for reference:

**Soccer:**
- Tottenham: 367, Arsenal: 359, Liverpool: 364, Man City: 382, Man United: 360
- Barcelona: 83, Real Madrid: 86, Bayern: 132, PSG: 160, Juventus: 111

**American Sports:**
- Lakers: 13, Warriors: 9, Celtics: 2 (NBA)
- Chiefs: 12, 49ers: 25, Cowboys: 6 (NFL)
- Maple Leafs: 10, Oilers: 22, Rangers: 4 (NHL)
- Yankees: 10, Dodgers: 19, Red Sox: 2 (MLB)

### 3. Create config.json

```bash
cp config.example.json config.json
```

Edit `config.json`:
```json
{
  "teams": [
    {
      "name": "Liverpool",
      "short_name": "Liverpool",
      "emoji": "🔴",
      "sport": "soccer",
      "espn_id": "364",
      "espn_leagues": ["eng.1", "uefa.champions"],
      "enabled": true
    },
    {
      "name": "Los Angeles Lakers",
      "short_name": "Lakers",
      "emoji": "🏀💜💛",
      "sport": "basketball",
      "espn_id": "13",
      "espn_leagues": ["nba"],
      "enabled": true
    },
    {
      "name": "Kansas City Chiefs",
      "short_name": "Chiefs",
      "emoji": "🏈",
      "sport": "football",
      "espn_id": "12",
      "espn_leagues": ["nfl"],
      "enabled": true
    }
  ],
  "alerts": {
    "goals": true,
    "red_cards": true,
    "halftime": true,
    "fulltime": true,
    "kickoff": true
  }
}
```

### 4. Test It

```bash
# Show ticker for your teams
python3 scripts/ticker.py

# Check live matches
python3 scripts/live_monitor.py --verbose

# View a specific league
python3 scripts/ticker.py league eng.1 soccer
python3 scripts/ticker.py league nfl football
python3 scripts/ticker.py league nba basketball

# ESPN API commands
python3 scripts/espn.py leagues           # List all sports/leagues
python3 scripts/espn.py leagues soccer    # List soccer leagues
python3 scripts/espn.py scoreboard nba basketball
python3 scripts/espn.py search "Lakers" basketball
```

## 📱 Example Alerts

**⚽ Soccer Goal:**
```
🎉 GOAL! 23'
⚽ Marcus Rashford (Manchester United)
Manchester United 1-0 Liverpool
```

**🏈 NFL Touchdown:**
```
🎉 TOUCHDOWN! Q2 3:42
🏈 Patrick Mahomes (Kansas City Chiefs)
Chiefs 14-7 Bills
```

**🏀 NBA 3-Pointer:**
```
🎉 3-POINTER! Q3 8:15
🎯 LeBron James (Los Angeles Lakers)
Lakers 78-72 Warriors
```

**🏒 NHL Goal:**
```
🎉 GOAL! P2 12:34
🏒 Connor McDavid (Edmonton Oilers)
Oilers 3-2 Maple Leafs
```

**Final Score:**
```
🏁 FINAL - WIN! 🎉✅ 🏈
Kansas City Chiefs 31-24 Buffalo Bills
```

## 🤖 Clawdbot Integration

### Auto-Scheduling (Match Day Alerts)

Create a daily cron job that checks for matches:

```javascript
// Morning check at 9 AM
{
  "name": "sports-match-check",
  "schedule": { "kind": "cron", "expr": "0 9 * * *", "tz": "Europe/London" },
  "payload": {
    "message": "Check if any configured teams play today. If yes, create a live ticker cron for the match window."
  }
}
```

### Live Ticker Cron

During matches, run every 2 minutes:
```bash
python3 scripts/live_monitor.py
```

The script only outputs when there are new events (goals, cards, etc.), making it perfect for cron-based alerting.

## 🔧 Scripts Reference

| Script | Purpose |
|--------|---------|
| `ticker.py` | Show current status of your teams |
| `live_monitor.py` | Check for live updates (for cron) |
| `espn.py` | Direct ESPN API access |
| `setup.py` | Interactive setup wizard |
| `config.py` | Configuration management |

## 🌐 ESPN API Reference

Base URL: `https://site.api.espn.com/apis/site/v2/sports`

### Endpoints

```bash
# Scoreboard (all today's games)
/{sport}/{league}/scoreboard

# Game details with events
/{sport}/{league}/summary?event={event_id}

# Team info
/{sport}/{league}/teams/{team_id}
```

### Sport & League Codes

**Soccer:** `soccer/eng.1`, `soccer/esp.1`, `soccer/uefa.champions`
**Football:** `football/nfl`
**Basketball:** `basketball/nba`, `basketball/wnba`
**Hockey:** `hockey/nhl`
**Baseball:** `baseball/mlb`
**Racing:** `racing/f1`

## 📄 License

MIT — use it however you want!

## 📚 ESPN API Resources

- [Public ESPN API Documentation](https://github.com/pseudo-r/Public-ESPN-API) — comprehensive endpoint list
- [ESPN OpenAPI Spec](https://github.com/zuplo/espn-openapi) — formal OpenAPI/Swagger schema
- [Interactive API Explorer](https://zudoku.dev/demo?api-url=https://raw.githubusercontent.com/zuplo/espn-openapi/refs/heads/main/espn_openapi_soccer_league_path.yaml) — try endpoints in browser
- [Zuplo Guide](https://zuplo.com/learning-center/espn-hidden-api-guide) — overview & alternatives

> ⚠️ **Note:** ESPN's API is unofficial/undocumented. It's stable and widely used, but could change without notice. The skill handles errors gracefully.

## 🙏 Credits

- ESPN for their awesome (and free!) API
- pseudo-r, zuplo, and the community for API documentation
- Built with ❤️ for football fans everywhere

---

Happy tracking! ⚽🏆
