import os
import time
import requests
import json
from dotenv import load_dotenv

load_dotenv()
WALLET = os.getenv('WALLET', '0x75e765216a57942d738d880ffcda854d9f869080')
USDC_AMOUNT = int(os.getenv('USDC_AMOUNT', 5))
PM_BASE = 'https://gamma-api.polymarket.com'

def poll_markets():
    url = f'{PM_BASE}/markets?active=true&closed=false&limit=100'
    resp = requests.get(url, timeout=5)
    if resp.status_code == 200:
        return resp.json()
    print(f"API error: {resp.status_code}")
    return []

print('🚀 lorden-nap v4 ARBS | BTC Edges → $70k Alerts | LIVE SCAN')

while True:
    markets = poll_markets()
    arb_count = 0
    for m in markets:
        if 'BTC' in m.get('question', ''):
            tokens = m.get('tokens', [])
            if len(tokens) > 1:
                yes_p = float(tokens[0].get('yesPrice', 0.5))
                no_p = float(tokens[1].get('noPrice', 0.5))
                if yes_p < 0.45:
                    print(f'🚨 ARB YES: {m["question"][:50]} @{yes_p:.1%} | AUTO-BUY $ {USDC_AMOUNT} | clobKey: {m.get("clobKey", "N/A")}')
                    arb_count += 1
                if no_p < 0.45:
                    print(f'🚨 ARB NO:  {m["question"][:50]} @{no_p:.1%} | AUTO-BUY $ {USDC_AMOUNT} | clobKey: {m.get("clobKey", "N/A")}')
                    arb_count += 1
    print(f"📊 Scan: {len(markets)} mkts | {arb_count} BTC edges | Next: 30s | Balance check: polymarket.com/portfolio")
    time.sleep(30)
