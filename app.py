import os
import time
import requests
import json
from dotenv import load_dotenv
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs
from py_clob_client.order_builder.constants import BUY  # FIXED IMPORT [web:27]

load_dotenv()
WALLET = os.getenv('WALLET', '0x75e765216a57942d738d880ffcda854d9f869080')
STRATEGY = os.getenv('STRATEGY', 'LATENCY_ARB')
USDC_AMOUNT = int(os.getenv('USDC_AMOUNT', 5))
PM_BASE = 'https://gamma-api.polymarket.com'

# ClobClient - needs PRIVATE_KEY env var
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
clob_client = None
if PRIVATE_KEY:
    clob_client = ClobClient(
        host="https://clob.polymarket.com",
        key=PRIVATE_KEY,
        chain_id=137
    )
    print("✅ ClobClient LOADED")
else:
    print("⚠️  No PRIVATE_KEY - ARBs print only (add to Railway env)")

def poll_markets():
    url = f'{PM_BASE}/markets?active=true&closed=false&limit=100'
    resp = requests.get(url, timeout=5)
    if resp.status_code == 200:
        return resp.json()
    print(f"API error: {resp.status_code}")
    return []

def clob_trade(m, side):  # 'YES' or 'NO'
    if not clob_client:
        print("❌ ClobClient missing - set PRIVATE_KEY")
        return
    tokens = m.get('tokens', [])
    if len(tokens) < 2:
        return
    token_idx = 0 if side == 'YES' else 1
    token_id = tokens[token_idx]['token_id']
    current_p = float(tokens[token_idx]['price'])
    price = int(current_p * 0.98 * (2**64))  # 2% edge, Q64.64 [web:14]
    
    order_args = OrderArgs(
        token_id=token_id,
        price=price,
        size=USDC_AMOUNT,
        side=BUY
    )
    
    try:
        # API creds auto (signs on first trade)
        clob_client.set_api_creds(clob_client.create_or_derive_api_creds())
        response = clob_client.post_order(order_args)
        print(f"🚀 LIVE TRADE TX: {response} | {side}")
    except Exception as e:
        print(f"Trade fail: {e}")

print('🚀 lorden-nap v4 | BTC ARBs → $70k | Clob Ready')

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
                    print(f'ARB YES: {m["question"][:40]} @{yes_p:.1%} | ${USDC_AMOUNT}')
                    # LIVE: clob_trade(m, 'YES')  # Uncomment Step 2
                    arb_count += 1
                if no_p < 0.45:
                    print(f'ARB NO: {m["question"][:40]} @{no_p:.1%} | ${USDC_AMOUNT}')
                    # LIVE: clob_trade(m, 'NO')
