import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
USDC_AMOUNT = 10
PM_BASE = 'https://gamma-api.polymarket.com'

def poll_events():
    url = f'{PM_BASE}/events?active=true&closed=false&limit=100'
    resp = requests.get(url, timeout=10)
    if resp.status_code == 200:
        events = resp.json()
        markets = []
        for e in events:
            markets.extend(e.get('markets', []))
        return markets
    print(f"Events error: {resp.status_code}")
    return []

print('🚀 lorden-nap v4.3 DEBUG | REAL-TIME EDGES | $70k')

markets_checked = 0
while True:
    markets = poll_events()
    print(f"\n🔍 DEBUG: Fetched {len(markets)} markets from events")
    
    # Print first 5 questions to see format
    for i, m in enumerate(markets[:5]):
        print(f"  {i+1}. Q: {m.get('question', 'NO_Q')[:80]}")
    
    edges = 0
    for m in markets:
        markets_checked += 1
        q = m.get('question', '').upper()
        tokens = m.get('tokens', [])
        if len(tokens) > 1:
            yes_p = float(tokens[0].get('yesPrice', 0.5))
            no_p = float(tokens[1].get('noPrice', 0.5))
            
            # ANY misprice >2%
            if abs(yes_p + no_p - 1.0) > 0.02 or min(yes_p, no_p) < 0.48:
                side = 'YES' if yes_p < no_p else 'NO'
                print(f"🚨 EDGE: {m['question'][:60]} | {side} {min(yes_p,no_p):.1%} | key={m.get('clobKey')}")
                edges += 1
    
    print(f"📊 Checked {markets_checked} | Edges: {edges} | Sleep 20s")
    time.sleep(20)
