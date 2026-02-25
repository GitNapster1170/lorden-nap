import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
USDC_AMOUNT = 10
PM_BASE = 'https://gamma-api.polymarket.com'

def poll_markets():
    # Direct markets + short-term tag filter
    url = f'{PM_BASE}/markets?active=true&closed=false&limit=500&tag_slug=crypto&tag_slug=sports'
    resp = requests.get(url, timeout=10)
    if resp.status_code == 200:
        return resp.json()
    # Fallback events
    url = f'{PM_BASE}/events?active=true&limit=100'
    resp = requests.get(url, timeout=10)
    if resp.status_code == 200:
        events = resp.json()
        markets = []
        for e in events:
            markets.extend(e.get('markets', []))
        return markets
    return []

print('🚀 v4.4 SHORT-TERM | 5MIN/NBA/ETH → $70k | HIGH-FREQ EDGES')

while True:
    markets = poll_markets()
    print(f"🔍 {len(markets)} markets | Short-term scan")
    
    short_count = edges = 0
    for m in markets:
        q = m.get('question', '').lower()
        tokens = m.get('tokens
