# Satellite Slugger

A browser batting game for broadband providers. Time your swing, launch the ball into low Earth orbit, and knock satellite internet out of the sky.

## Play

- **Swing:** Space, tap the field, or press the Swing button
- **Aim with timing:** early swing = line drive (low orbit), late swing = moonshot (high orbit)
- **Gigabit Swing:** every 6 satellites charges a fiber laser that clears everything on its line
- Three strikes is an out. Three outs ends the game.

## Rebrand

Edit the constants at the top of the script in `index.html`:

```js
const BRAND = 'Your Local Fiber';
const JERSEY = 'FIBER';
const CTA_TEXT = 'Check fiber at your address';
const CTA_URL = '';   // set this to show a call-to-action button on the game-over screen
```

## Deploy

It's a single static `index.html` with no build step. On Vercel, import the repo and deploy with the default settings (Framework preset: Other).

## Leaderboard

Players who make the top 10 enter three initials, arcade style. Scores are shared through `api/scores.js`, a Vercel function that stores them in Upstash Redis.

To turn it on:

1. In the Vercel project, open **Storage** (or **Integrations → Marketplace**) and add **Upstash for Redis** (the free tier is plenty).
2. Connect it to this project, for **Production** (and Preview if you want). It adds the `KV_REST_API_URL` and `KV_REST_API_TOKEN` environment variables. The `UPSTASH_REDIS_REST_*` names, a custom prefix (e.g. `STORAGE_KV_REST_API_URL`), or just an Upstash `REDIS_URL` / `KV_URL` all work too.
3. Redeploy. Environment variables only reach new deployments.
4. Check `https://<your-site>/api/scores`. It should return `{"scores":[...]}`. If it says storage isn't connected, the variables aren't reaching the deployment yet.

Until storage is connected, the board quietly falls back to scores saved on each player's device.

Optional: set `LEADERBOARD_KEY` to give a provider its own board (e.g. `acmefiber:board`) when several deployments share one Redis database.

Built-in protections: three letters only, a small blocklist for rude initials, a basic score sanity check, and a limit of 8 submissions per minute per IP. It's a fun board, not a cheat-proof one.
