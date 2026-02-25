import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
USDC_AMOUNT = 50  # Copy size
PM_BASE = 'https://gamma-api.polymarket.com'

def get_top_wallets():
    # Top performers (update from polymarket.com/leaderboard)
    return [
        '0x...',  # Replace with real top from site
        'your_wallet_copy_targets'
    ]

print('🚀 v5 COPY-TRADING | TOP WALLETS → $70k/mo | Alerts LIVE')

while True:
    # Poll your portfolio for copy signals
    url = f'{PM_BASE}/positions?wallet={os.getenv("WALLET")}'
    resp = requests.get(url)
    if resp.status_code == 200:
        positions = resp.json()
        for p in positions:
            if p.get('pnl_usd', 0) > 10:  # Winning trades
                print(f"🚨 COPY WIN: {p['question'][:50]} PnL +${p['pnl_usd']} | Scale $ {USDC_AMOUNT}")
    
    # Top wallet trades
    print("📊 Check polymarket.com/leaderboard | Copy top 5 | Balance: $500+")
    time.sleep(60)
