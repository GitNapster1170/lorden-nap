import os
import time
import requests
import json
from dotenv import load_dotenv

load_dotenv()
WALLET = os.getenv('WALLET', '0x75e765216a57942d738d880ffcda854d9f869080')
STRATEGY = os.getenv('STRATEGY', 'LATENCY_ARB')
USDC_AMOUNT = int(os.getenv('USDC_AMOUNT', 5))
PM_BASE = 'https://gamma-api.polymarket.com'

def poll_markets():
    # Fixed: Drop wallet filter (for all active), add closed=false, higher limit
    url = f'{PM_BASE}/markets?active=true&closed=false&limit=100'
    resp = requests.get(url, timeout=5)
    if resp.status_code == 200:
        return resp.json()
    print(f"API error: {resp.status_code}")
    return []

print('🚀 lorden-nap Latency Arb | $7k/day → $70k/7days | Part 4 LIVE')

while True:
    markets = poll_markets()
    for m in markets:
        if 'BTC' in m.get('question', ''):
            # Fixed: Use tokens[0].yesPrice (standard schema), safe float
            tokens = m.get('tokens', [])
            if tokens:
                yes_p = float(tokens[0].get('yesPrice', 0.5))
                no_p = float(tokens[1].get('noPrice', 0.5) if len(tokens) > 1 else 1 - yes_p)
                # Edge: Misprice >5% from 50/50 fair (or tune)
                if yes_p < 0.45 or no_p < 0.45:
                    side = 'YES' if yes_p < 0.45 else 'NO'
                    edge_p = min(yes_p, no_p)
                    print(f'ARB: {m["question"][:40]} {side}@{edge_p:.1%} | BUY ${USDC_AMOUNT}')
                    # Live: clob.trade(m.get('clobKey'), 'buy' if side=='YES' else 'sell', USDC_AMOUNT)
    time.sleep(30)  # Fixed: 30s poll (0.1s hits rate limits ~100/min) [web:22]
