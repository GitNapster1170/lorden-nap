import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
USDC_AMOUNT = int(os.getenv('USDC_AMOUNT', 10))  # $10 trades
PM_BASE = 'https://gamma-api.polymarket.com'

def poll_markets():
    url = f'{PM_BASE}/markets?active=true&closed=false&limit=500'  # Max scan
    resp = requests.get(url, timeout=10)
    if resp.status_code == 200:
        return resp.json()
    print(f"API error: {resp.status_code}")
    return []

print('🚀 lorden-nap v4.2 | ALL EDGES → $70k | NBA/ETH/BTC LIVE')

while True:
    markets = poll_markets()
    crypto_count = nba_count = arb_count = 0
    for m in markets:
        q = m.get('question', '').upper()
        tokens = m.get('tokens', [])
        if len(tokens) < 2: continue
        
        yes_p = float(tokens[0].get('yesPrice', 0.5))
        no_p = float(tokens[1].get('noPrice', 0.5))
        
        # Tags
        is_crypto = any(kw in q for kw in ['BTC', 'BITCOIN', 'ETH', 'SOLANA', 'CRYPTO'])
        is_nba = 'NBA' in q or any(team in q for team in ['Lakers', 'Celtics', 'Bulls', 'Knicks'])
        
        if is_crypto:
            crypto_count += 1
            print(f"CRYPTO: {m['question'][:60]} | Yes{yes_p:.0%} No{no_p:.0%}")
        if is_nba:
            nba_count += 1
            print(f"NBA: {m['question'][:60]} | Yes{yes_p:.0%} No{no_p:.0%}")
        
        # ANY edge <49% (1% misprice)
        if min(yes_p, no_p) < 0.49:
            side = 'YES' if yes_p < no_p else 'NO'
            print(f"🚨 EDGE {side}: {m['question'][:50]} @{min(yes_p,no_p):.1%} | $ {USDC_AMOUNT} | key={m.get('clobKey', 'N/A')}")
            arb_count += 1
    
    print(f"📊 {len(markets)} mkts | Crypto:{crypto_count} NBA:{nba_count} | Edges:{arb_count} | Check: polymarket.com/crypto")
    time.sleep(20)  # Faster 20s
