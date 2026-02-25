import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
PRIVATE_KEY = os.getenv('PRIVATE_KEY')  # 64 hex NOW
WALLET = os.getenv('WALLET')
USDC_AMOUNT = 50

from py_clob_client.client import ClobClient
clob_client = ClobClient("https://clob.polymarket.com", key=PRIVATE_KEY, chain_id=137)

def get_top_wallets():
    resp = requests.get("https://data-api.polymarket.com/v1/leaderboard?period=monthly")  # Top profit [web:80]
    if resp.status_code == 200:
        return [trader['proxyWallet'] for trader in resp.json()[:3]]  # Top 3
    return ['0x492442EaB586F242B53bDa933fD5dE859c8A3782']  # Fallback [web:61]

def copy_latest_trade(target_wallet):
    # Get target recent position
    url = f"https://gamma-api.polymarket.com/positions?wallet={target_wallet}&limit=1"
    resp = requests.get(url)
    if resp.status_code == 200 and resp.json():
        pos = resp.json()[0]
        token_id = pos['token_id']
        side = 'BUY' if pos['outcomeIndex'] == 0 else 'SELL'
        price = int(0.5 * 2**64)  # Market price approx
        order_args = OrderArgs(token_id=token_id, price=price, size=USDC_AMOUNT, side=side)
        clob_client.post_order(order_args)
        print(f"🚀 COPIED {target_wallet}: {pos['question'][:50]} ${USDC_AMOUNT}")

print('🚀 AUTO COPY BOT v6 | Leaderboard Top 3 → $70k | LIVE')

while True:
    tops = get_top_wallets()
    for wallet in tops:
        copy_latest_trade(wallet)
        time.sleep(10)
    print("Cycle complete | Check portfolio")
    time.sleep(300)  # 5min
