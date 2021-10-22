
import datetime as dt



start = dt.datetime(2020, 9, 10)
end = dt.datetime.now()



def ema_fast(prices, days, smoothing=2):

        ema = [sum(prices[:days]) / days]
        for price in prices[days:]:
            ema.append((price * (smoothing / (1 + days))) + ema[-1] * (1 - (smoothing / (1 + days))))
        return ema[len(ema) - 1]

def ema_med(prices, days, smoothing=2):

        ema = [sum(prices[:days]) / days]
        for price in prices[days:]:
            ema.append((price * (smoothing / (1 + days))) + ema[-1] * (1 - (smoothing / (1 + days))))
        return ema[len(ema) - 1]

def ema_slow(prices, days, smoothing=2):

        ema = [sum(prices[:days]) / days]
        for price in prices[days:]:
            ema.append((price * (smoothing / (1 + days))) + ema[-1] * (1 - (smoothing / (1 + days))))
        return ema[len(ema) - 1]
