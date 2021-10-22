
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

#ema = ema_fast(data['Close'], 10)
#ema_medium = ema_med(data['Close'], 26)
#ema_slowy = ema_slow(data['Close'], 72)


#price_X = np.arange(data.shape[0])        # Creates array [0, 1, 2, 3, 4, 5]
#ema_x = np.arange(10, data.shape[0]+1)    # Array from [10, 11, 12, 13]
#ema_2 = np.arange(26, data.shape[0]+1)
#ema_3 = np.arange(72, data.shape[0]+1)


#plt.xlabel('Days')
#plt.ylabel('Price')
#plt.plot(price_X, data['Close'], label = 'Close boy', color= 'red')
#plt.plot(ema_x, ema, label = 'EMA_10_FAST', color = 'yellow')
#plt.plot(ema_3, ema_slowy, label = 'EMA_72_SLOW', color = 'blue')
#plt.plot(ema_2, ema_medium, label = 'EMA_26_MED', color = 'green')
#lt.legend()
#plt.show()





