import time

from scanner import get_trending_tokens
from discord_webhook import send_discord

while True:

    try:

        tokens = get_trending_tokens()

        msg = "🔥 TRENDING TOKENS (CoinGecko)\n\n"

        for i, coin in enumerate(tokens[:10], 1):

            msg += (
                f"{i}. {coin['name']} ({coin['symbol']})\n"
            )

        send_discord(msg)

        print("sent")

    except Exception as e:

        print("ERROR:", e)

    time.sleep(300)
