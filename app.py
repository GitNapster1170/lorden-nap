import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
USDC_AMOUNT = 10
PM_BASE = 'https://gamma-api.polymarket.com'

def poll_markets():
    # Try crypto/sports tags
    for tag in ['crypto', 'sports', 'nba']:
        url = f'{PM_BASE}/markets?active=true&closed=false&limit=100&tag_slug={tag}'
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200 and resp.json():
            return resp.json()
    # Fallback all
    url = f'{PM_BASE}/markets?active=true&closed=false&limit=500'
    resp = requests.get(url, timeout=10)
    return resp.json() if resp.status_code == 200 else []

print('🚀 v4.4 SHORT-TERM | NBA/5MIN → $70k | PERFECT')

while True:
    markets = poll_markets()
    print(f"🔍 {len(markets)} markets loaded")
    
    short = edges = 0
    for m in markets:
        q = m.get('question', '').lower()
        tokens = m.get('tokens', [])
        if len(tokens) < 2: continue
        
        yes_p = float(tokens[0].get('yesPrice', 0.5))
        no_p = float(tokens[1].get('noPrice', 0.5))
        
        # Short-term keywords
        if any(word in q for word in ['5min', '5m', '15min', '15m', 'hour', 'today', 'nba', 'spread']):
            short += 1
            print(f"SHORT: {m['question'][:70]} | Yes{yes_p:.1%} No{no_p:.1%}")
            
            if min(yes_p, no_p) < 0.48 or abs(yes_p + no_p - 1) > 0.03:
                print(f"🚨 TRADE: {m['question'][:50]} | Edge {min(yes_p,no_p):.1%} | $ {USDC_AMOUNT} clob={m.get('clobKey')}")
                edges += 1
    
    print(f"📊 Short-term: {short} | Edges: {edges} | Next 20s")
    time.sleep(20)
