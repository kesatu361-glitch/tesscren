import ccxt
import pandas as pd
import ta

binance = ccxt.binance({"options": {"defaultType": "future"}})
bybit = ccxt.bybit({"options": {"defaultType": "swap"}})

def get_pairs(exchange):
    markets = exchange.load_markets()
    return [s for s in markets if "/USDT" in s]

def analyze(exchange, symbol):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe="5m", limit=100)
        df = pd.DataFrame(ohlcv, columns=["time","open","high","low","close","volume"])

        df["ema20"] = ta.trend.EMAIndicator(df["close"], 20).ema_indicator()
        df["ema50"] = ta.trend.EMAIndicator(df["close"], 50).ema_indicator()
        df["rsi"] = ta.momentum.RSIIndicator(df["close"], 14).rsi()

        score = 0

        current_volume = df["volume"].iloc[-1]
        avg_volume = df["volume"].tail(20).mean()

        if current_volume > avg_volume * 1.5:
            score += 2

        if df["ema20"].iloc[-1] > df["ema50"].iloc[-1]:
            score += 2

        rsi = df["rsi"].iloc[-1]
        if 55 <= rsi <= 75:
            score += 2

        resistance = df["high"].tail(20).max()
        if df["close"].iloc[-1] >= resistance:
            score += 3

        return {
            "symbol": symbol,
            "score": score,
            "price": round(df["close"].iloc[-1], 6),
            "rsi": round(rsi, 2)
        }
    except Exception:
        return None
