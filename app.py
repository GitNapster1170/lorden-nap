import os
import time
import requests
import json
from dotenv import load_dotenv
from py_clob_client.client import ClobClient
from py_clob_client.constants import BUY, SELL
from py_clob_client.clob_types import OrderArgs

load_dotenv()
WALLET = os.getenv('WALLET', '0x75e765216a57942d738d880ffcda854d9f869080')
STRATEGY = os.getenv('STRATEGY', 'LATENCY_ARB')
USDC_AMOUNT = int(os.getenv('USDC_AMOUNT', 5))
PM_BASE = 'https://gamma-api.polymarket.com'

# ClobClient setup - ADD YOUR PRIVATE_KEY to Railway env vars
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
if not PRIVATE_KEY:
    print("🚨 MISSING PRIVATE_KEY env var - add to Railway!")
else:
    clob_client = ClobClient(
        host="https://clob.polymarket.com",
        key=PRIVATE_KEY,
        chain_id=137  # Polygon
    )
    print("✅ ClobClient READY")

def poll_markets():
    url = f'{PM_BASE}/markets?active=true&closed=false&limit=100'
    resp = requests.get(url, timeout=5)
    if resp.status_code == 200:
        return resp.json()
    print(f"API error: {resp.status_code}")
    return []

def clob_trade(m, side):  # side='YES' or 'NO'
    tokens = m['tokens']
    token_idx = 0 if side == 'YES' else 1
    token_id = tokens[token_idx]['token_id']
    
    # Edge price: 2% better
    current_p = float(tokens[token_idx]['price'])
    edge_price = current_p * 0.98  # Buy low
    price = int(edge_price * (2**64))  # Q64.64 [web:14]
    
    order_args = OrderArgs(
        token_id=token_id,
        price=price,
        size=USDC_AMOUNT,
        side=BUY
    )
    
    try:
        response = clob_client.post_order(order_args)
        print(f"🚀 LIVE TRADE: {response.get('order_id')} | {m['question'][:40]} {side} ${USDC_AMOUNT}")
        return response
    except Exception as e:
        print(f"Trade error: {e}")

print('🚀 lorden-nap Latency Arb | $7k/day → $70k/7days | Part 4 STEPS LIVE')

while True:
    markets = poll_markets()
    arb_count = 0
    for m in markets:
        if 'BTC' in m.get('question', ''):
            tokens = m.get('tokens', [])
            if tokens and len(tokens) > 1:
                yes_p = float(tokens[0].get('yesPrice', 0.5))
                no_p = float(tokens[1].get('noPrice', 0.5))
                if yes_p < 0.45:
                    print(f'ARB: {m["question"][:40]} YES@{yes_p:.1%} | BUY ${USDC_AMOUNT}')
                    # LIVE: clob_trade(m, 'YES')  # UNCOMMENT AFTER TEST
                    arb_count += 1
                elif no_p < 0.45:
                    print(f'ARB: {m["question"][:40]} NO@{no_p:.1%} | BUY ${USDC_AMOUNT}')
                    # LIVE: clob_trade(m, 'NO')
                    arb_count += 1
    print(f"Scan complete: {len(markets)} markets, {arb_count} BTC edges")
    time.sleep(30)
