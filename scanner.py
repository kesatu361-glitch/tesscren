import requests

def get_trending_tokens():

    url = "https://api.coingecko.com/api/v3/search/trending"

    response = requests.get(url, timeout=20)

    data = response.json()

    results = []

    for coin in data["coins"]:

        item = coin["item"]

        results.append({
            "symbol": item["symbol"],
            "name": item["name"],
            "score": item.get("market_cap_rank", 9999)
        })

    return results
