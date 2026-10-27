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
