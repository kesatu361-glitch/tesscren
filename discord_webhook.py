import requests
import os

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def send_discord(message):
    try:
        requests.post(WEBHOOK, json={"content": message}, timeout=10)
    except Exception as e:
        print(e)
