import random
import numpy as np

class TradingBot:
    def __init__(self):
        self.prices = []
        self.window_size = 14  # RSI ინდიკატორისთვის
        self.sma_period = 50  # Moving Average

    def calculate_rsi(self):
        if len(self.prices) < self.window_size:
            return None
        deltas = np.diff(self.prices)
        gains = deltas[deltas > 0].sum() / self.window_size
        losses = -deltas[deltas < 0].sum() / self.window_size
        rs = gains / losses if losses != 0 else 100  # Avoid division by zero
        return 100 - (100 / (1 + rs))

    def calculate_macd(self):
        if len(self.prices) < 26:  # MACD-სთვის საჭიროა უფრო დიდი მონაცემები
            return None
        short_term_ema = self.calculate_ema(12)
        long_term_ema = self.calculate_ema(26)
        return short_term_ema - long_term_ema

    def calculate_ema(self, period):
        weights = np.exp(np.linspace(-1., 0., period))
        weights /= weights.sum()
        return np.dot(self.prices[-period:], weights)

    def get_market_signal(self):
        price = random.uniform(1, 100)  # შემთხვევითი ფასის გენერაცია
        self.prices.append(price)
        if len(self.prices) > 100:
            self.prices.pop(0)  # მაქსიმუმ 100 წინა მონაცემი

        rsi = self.calculate_rsi()
        macd = self.calculate_macd()

        if rsi and rsi < 30:
            signal = "Market oversold (buy signal)"
        elif rsi and rsi > 70:
            signal = "Market overbought (sell signal)"
        elif macd and macd > 0:
            signal = "Market bullish"
        elif macd and macd < 0:
            signal = "Market bearish"
        else:
            signal = "Market is stable"

        return {
            "signal": signal,
            "market_value": price,
            "rsi": rsi,
            "macd": macd
        }

bot = TradingBot()

# ვთქვათ, რომ ბოტი ყოველ 1 წუთში ანალიზს აკეთებს
signal = bot.get_market_signal()
print(signal)
