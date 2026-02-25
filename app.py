import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
USDC_AMOUNT = int(os.getenv('USDC_AMOUNT', 5))
PM_BASE = 'https://gamma-api.polymarket.com'

def poll_markets():
    url = f'{PM_BASE}/markets?active=true&closed=false&limit=200'  # More markets
    resp = requests.get(url, timeout=5)
    if resp.status_code == 200:
        return resp.json()
    print(f"API error: {resp.status_code}")
    return []

print('🚀 lorden-nap v4.1 | CRYPTO ARBs → $70k | Edges LIVE')

while True:
    markets = poll_markets()
    btc_count = 0
    arb_count = 0
    for m in markets:
        q = m.get('question', '').upper()
        if any(kw in q for kw in ['BTC', 'BITCOIN']):
            btc_count += 1
            tokens = m.get('tokens', [])
            if len(tokens) > 1:
                yes_p = float(tokens[0].get('yesPrice', 0.5))
                no_p = float(tokens[1].get('noPrice', 0.5))
                print(f"BTC: {m['question'][:60]} | Yes {yes_p:.1%} No {no_p:.1%}")
                if yes_p < 0.47 or no_p < 0.47:  # Looser 3% edge
                    side = 'YES' if yes_p < 0.47 else 'NO'
                    print(f"🚨 ARB {side}: {m['question'][:50]} @{min(yes_p,no_p):.1%} | TRADE $ {USDC_AMOUNT} clobKey={m.get('clobKey')}")
                    arb_count += 1
    print(f"📊 {len(markets)} mkts | {btc_count} BTC | {arb_count} edges | polymarket.com/crypto")
    time.sleep(30)
