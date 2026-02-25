import os
import time
import requests
from dotenv import load_dotenv
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs
from py_clob_client.order_builder.constants import BUY  # FIXED [web:25]

load_dotenv()
PRIVATE_KEY = '8db8635db5b87088c224ee1e017f3bfb165158044c2adae55c419fccf7fdf695'
USDC_AMOUNT = 50

clob_client = ClobClient("https://clob.polymarket.com", key=PRIVATE_KEY, chain_id=137)
print("✅ KEY LOADED | BOT TRADING")

def find_edges():
    resp = requests.get("https://gamma-api.polymarket.com/markets?active=true&limit=100")
    if resp.status_code != 200:
        return []
    markets = resp.json()
    edges = []
    for m in markets:
        tokens = m.get('tokens', [])
        if len(tokens) > 0:
            p = float(tokens[0].get('yesPrice', 0.5))
            if p < 0.48:
                token_id = tokens[0]['token_id']
                price = int(p * 2**64)
                edges.append((token_id, price))
    return edges

print('🚀 FULL AUTO BOT | EDGES → TRADES | $70k')

while True:
    edges = find_edges()
    for token_id, price in edges[:2]:
        order_args = OrderArgs(
            token_id=token_id,
            price=price,
            size=USDC_AMOUNT,
            side=BUY
        )
        try:
            tx = clob_client.post_order(order_args)
            print(f"✅ TRADE LIVE: {token_id[:16]}... $50 TX:{tx.get('order_id', 'pending')}")
        except Exception as e:
            print(f"Trade skip: {e}")
    print("Cycle done | Portfolio refresh")
    time.sleep(120)
