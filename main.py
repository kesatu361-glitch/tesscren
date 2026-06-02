import time
from dotenv import load_dotenv
from scanner import binance, bybit, get_pairs, analyze
from discord_webhook import send_discord

load_dotenv()

def scan_exchange(exchange):
    results = []
    pairs = get_pairs(exchange)

    for symbol in pairs[:150]:
        data = analyze(exchange, symbol)
        if data:
            results.append(data)

    return results

while True:
    try:
        data = []
        data.extend(scan_exchange(binance))
        data.extend(scan_exchange(bybit))

        top = sorted(data, key=lambda x: x["score"], reverse=True)[:10]

        msg = "🔥 TOP 10 TOKEN PANAS\n\n"

        for i, coin in enumerate(top, 1):
            msg += (
                f"{i}. {coin['symbol']}\n"
                f"Score: {coin['score']}/10\n"
                f"Price: {coin['price']}\n"
                f"RSI: {coin['rsi']}\n\n"
            )

        send_discord(msg)
        print("sent")

    except Exception as e:
        print(e)

    time.sleep(300)
