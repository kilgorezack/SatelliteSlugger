// Satellite Slugger leaderboard — Vercel serverless function backed by Upstash Redis (REST API).
// Connect "Upstash for Redis" from the Vercel Marketplace; it sets the env vars read below.
//   GET  /api/scores            -> { scores: [{ id, initials, score, kills }] }   (top 10)
//   POST /api/scores {initials, score, kills} -> { id, scores }

const REDIS_URL = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
const REDIS_TOKEN = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;
const KEY = process.env.LEADERBOARD_KEY || 'satslugger:board';
const KEEP = 500; // entries kept in storage; only the top 10 are shown

const BLOCKED = new Set(['ASS','FUK','FUC','FCK','SEX','KKK','NIG','NGR','FAG','CUM','TIT','DIK','DIC','COK','CNT','JIZ','WTF','POS','SHT','XXX','GAY','HOE','NAZ','KYS','PEE','POO']);

async function redis(commands) {
  const r = await fetch(`${REDIS_URL}/pipeline`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${REDIS_TOKEN}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(commands),
  });
  if (!r.ok) throw new Error(`Redis HTTP ${r.status}`);
  const out = await r.json();
  return out.map((x) => { if (x.error) throw new Error(x.error); return x.result; });
}

function toEntries(flat) {
  const list = [];
  for (let i = 0; i < flat.length; i += 2) {
    try {
      const m = JSON.parse(flat[i]);
      list.push({ id: m.id, initials: m.i, kills: m.k, score: Number(flat[i + 1]) });
    } catch (e) { /* skip malformed */ }
  }
  return list;
}

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  if (!REDIS_URL || !REDIS_TOKEN) {
    return res.status(503).json({ error: 'Leaderboard storage is not connected yet.' });
  }

  try {
    if (req.method === 'GET') {
      const [top] = await redis([['ZREVRANGE', KEY, 0, 9, 'WITHSCORES']]);
      return res.status(200).json({ scores: toEntries(top) });
    }

    if (req.method === 'POST') {
      let body = req.body;
      if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = {}; } }
      body = body || {};

      const initials = String(body.initials || '').toUpperCase();
      const score = Number(body.score);
      const kills = Number(body.kills);

      if (!/^[A-Z]{3}$/.test(initials)) return res.status(400).json({ error: 'Initials need to be three letters.' });
      if (BLOCKED.has(initials)) return res.status(400).json({ error: 'Let’s keep it family-friendly. Pick different initials.' });
      // Light sanity check: points come from satellites (max ~1,200 each with combos + storms) plus small perfect-swing bonuses.
      if (!Number.isInteger(score) || !Number.isInteger(kills) || score < 1 || kills < 0 || kills > 5000 || score > kills * 1300 + 25000) {
        return res.status(400).json({ error: 'That score doesn’t add up.' });
      }

      const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
      const rlKey = `satslugger:rl:${ip}`;
      const [hits] = await redis([['INCR', rlKey], ['EXPIRE', rlKey, 60]]);
      if (hits > 8) return res.status(429).json({ error: 'Too many scores in a minute. Take a breather.' });

      const id = Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
      const member = JSON.stringify({ id, i: initials, k: kills });
      const [, , top] = await redis([
        ['ZADD', KEY, score, member],
        ['ZREMRANGEBYRANK', KEY, 0, -(KEEP + 1)],
        ['ZREVRANGE', KEY, 0, 9, 'WITHSCORES'],
      ]);
      return res.status(200).json({ id, scores: toEntries(top) });
    }

    res.setHeader('Allow', 'GET, POST');
    return res.status(405).json({ error: 'Method not allowed.' });
  } catch (err) {
    console.error('leaderboard error', err);
    return res.status(500).json({ error: 'The leaderboard is having a moment. Try again.' });
  }
};
