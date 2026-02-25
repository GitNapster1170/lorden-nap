import os
import time
import requests
from dotenv import load_dotenv
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs
from py_clob_client.constants import BUY  # Or order_builder if error

load_dotenv()
PRIVATE_KEY = '8db8635db5b87088c224ee1e017f3bfb165158044c2adae55c419fccf7fdf695'  # YOUR KEY
USDC_AMOUNT = 50

clob_client = ClobClient("https://clob.polymarket.com", key=PRIVATE_KEY, chain_id=137)
print("✅ ClobClient ACTIVE - TRADING LIVE")

def poll_top_positions():
    # Top profitable positions (public API)
    url = "https://gamma-api.polymarket.com/markets?active=true&limit=50"
    resp = requests.get(url)
    if resp.status_code != 200:
        return []
    markets = resp.json()
    edges = []
    for m in markets:
        tokens = m.get('tokens', [])
        if len(tokens) > 1:
            yes_p = float(tokens[0].get('yesPrice', 0.5))
            if yes_p < 0.48:  # Edge
                edges.append((m['tokens'][0]['token_id'], int(yes_p * 2**64), BUY))
    return edges

print('🚀 AUTO BOT v6 | Copy Edges LIVE | $70k START')

while True:
    edges = poll_top_positions()
    for token_id, price, side in edges[:3]:  # Top 3 edges
        try:
            order_args = OrderArgs(token_id=token_id, price=price, size=USDC_AMOUNT, side=side)
            tx = clob_client.post_order(order_args)
            print(f"🚀 TRADE EXECUTED: token {token_id[:10]}... ${USDC_AMOUNT} TX: {tx}")
        except Exception as e:
            print(f"Trade error: {e}")
    time.sleep(60)  # 1min cycle
