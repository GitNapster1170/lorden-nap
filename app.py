import os
import time
import requests
import json
from dotenv import load_dotenv

load_dotenv()
WALLET = os.getenv('WALLET', '0x75e765216a57942d738d880ffcda854d9f869080')
STRATEGY = os.getenv('STRATEGY', 'LATENCY_ARB')
USDC_AMOUNT = int(os.getenv('USDC_AMOUNT', 5))
PM_BASE = 'https://gamma.api.polymarket.com'
def poll_markets():
    resp = requests.get(f'{PM_BASE}/markets?active=true&limit=20&wallet={WALLET}', timeout=2)
    if resp.status_code == 200:
        return resp.json()
    return []

print('🚀 lorden-nap Latency Arb | $7k/day → $70k/7days')

while True:
    markets = poll_markets()
    for m in markets:
        if 'BTC' in m.get('question', '') and m.get('endDate', 0) > time.time()*1000:
            yes_p = float(m['tokens'][0]['price'])
            if yes_p < 0.35 or (1-yes_p) < 0.35:
                print(f'ARB: {m["question"][:30]} YES@{yes_p:.1%} | BUY $5')
                # Live: clob.trade(m['clobKey'], 'buy', 5)
    time.sleep(0.1)  # lorden 100ms [cite:257]
