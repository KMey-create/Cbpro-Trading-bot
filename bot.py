import cbpro
import random
import pandas as pd
import time
import ema_calculator
import datetime as dt
import logging
import json


### Logger  ###
today = dt.datetime.today()
filename = f"{today.month:02d}-{today.day}-{today.year}.log"
loger = logging.getLogger('JustALogger')
formatter = logging.Formatter('%(asctime)s %(threadName)12s: %(message)s')

filehandler = logging.FileHandler(filename)
filehandler.setLevel(logging.DEBUG)
filehandler.setFormatter(formatter)
loger.addHandler(filehandler)

loger.setLevel(logging.DEBUG)
### Logger  ###


with open('orders.json', 'r') as filos:
    positions = json.loads(filos.read())




public = ''
passphrase = ''
secret = ''


auth_client = cbpro.AuthenticatedClient(key= public, passphrase= passphrase, b64secret= secret)


products_info = pd.DataFrame(auth_client.get_products())
#products = ['ADA-EUR', 'AAVE-EUR', 'DOT-EUR', 'EOS-EUR','LTC-EUR','EOS-EUR', 'LINK-EUR', 'OMG-EUR', 'SUSHI-EUR', 'WLUNA-EUR']
products = ['IOTX-BTC','CLV-USDT','GNT-USDC','MATIC-GBP','REN-USD','NMR-EUR','RLC-USD','ETH-USDC','REQ-USD','ADA-ETH','GTC-USD','SOL-USDT','BNT-GBP','SHIB-USD','CGLD-BTC','DOGE-USDT','ICP-BTC','ALGO-USD','DASH-BTC','BAL-BTC','GRT-EUR','MKR-USD','MANA-EUR','ICP-GBP','MIR-BTC','OMG-BTC','POLY-USD','RAD-GBP','ZRX-EUR','WBTC-BTC','BTRST-USDT','SUSHI-USD','FIL-GBP','WBTC-USD','MANA-USD','REQ-USDT','SNX-EUR','ETH-DAI','CLV-USD','XTZ-EUR','NMR-BTC','MKR-BTC','ATOM-USD','AAVE-GBP','BTC-GBP','1INCH-EUR','REP-USD','ALGO-GBP','RAD-EUR','MASK-EUR','XYO-EUR','SUSHI-ETH','BNT-EUR','ATOM-BTC','TRU-EUR','CHZ-GBP','REQ-BTC','ETH-EUR','UST-EUR','MATIC-EUR','BAT-EUR','LINK-EUR','LINK-BTC','CLV-EUR']
def RSI_calc(ticker):

    try:
        data = pd.DataFrame(auth_client.get_product_historic_rates(ticker, granularity= 86400), columns=['date','open','high','low','close','Dunno'])
        delta = data['close'].diff(1)
        delta.dropna(inplace = True)
        positive = delta.copy()
        negative = delta.copy()

        positive[positive < 0] = 0
        negative[negative > 0] = 0
        days = 14
        average_gain = positive.rolling(window = days).mean()
        average_loss = abs(negative.rolling(window = days).mean())
        relative_strength = average_gain / average_loss

        RSI = 100.0 - (100.0 / (1.0 + relative_strength))

        return round(RSI[len(RSI) - 1].item(), 3)


    except Exception as e:
        RSI = float(22.2222)
        print("SHT", e)
        return RSI

def set_direction(ticker):

        try:
                                                                            # [::-1]
            data_ticker = pd.DataFrame(auth_client.get_product_historic_rates(product_id= ticker, granularity= 86400), columns=['date','open','high','low','close','Dunno'])

            prices = data_ticker['close']

            #ema_fast = varis.ema_fast(prices, days= 10)
            ema_med = float(ema_calculator.ema_med(prices, days = 26))
            ema_slow = float(ema_calculator.ema_slow(prices, days= 78))

            x = float(data_ticker['close'][len(data_ticker['close']) - 25])

            y = float(data_ticker['close'][len(data_ticker['close']) - 1])
            #print(ticker, '::', x, '::', y, '::', '::', ema_slow, '::', ema_med)
            #print(ticker, 'Price-30::', type(x), 'Price-1::', type(y), 'EMAS::', type(ema_slow), 'EMAL::', type(ema_med))




            if ema_med > ema_slow and (y >= x):

                return "buy"

            elif ema_med < ema_slow and (x >= y):

                return "sell"

            elif ((ema_med or ema_slow) == None) and (x >= y):
                return "sell"

            else:
                return "buy"


        except Exception as e:

            print('Dir err ', ticker, '::-', e, ' -')


            return "buy"


def pos_handler():
    try:
        pos =random.choice(positions)
        id = pos['product_id']
        size = float(pos['size'])
        check_price = pos['price']
        tick = auth_client.get_product_ticker(id)['price']
        print(f"IMPORTANT! {id} :: {check_price} :: {size}")

        if tick >= check_price * 1.12:
            pos = auth_client.sell(size= size, product_id= id, order_type= 'market')
            time.sleep(1.1)
            loger.info("Selling from pos_handler")
            loger.info(pos)
            print(pos)
            positions.append(pos)
            print(positions)

        elif tick <= check_price * 0.885:
            order = auth_client.buy(product_id= id, order_type='market', size= size)
            time.sleep(1.1)
            loger.info("Buying from pos_handler")
            loger.info(pos)
            print(order)
            positions.append(order)
            print(positions)

    except Exception as e:
        print('pos_handler error ::- ', e, " --")





def main():
    while True:


        if len(positions) > 1:
            pos_handler()

        ticker= random.choice(products)
        price = float(auth_client.get_product_ticker(ticker)['bid'])
        rsi = RSI_calc(ticker)
        direction = set_direction(ticker)
        BASE = float(products_info[products_info['id'].str.fullmatch(ticker)]['base_min_size'])
        QUANTITY = float(products_info[products_info['id'].str.fullmatch(ticker)]['min_market_funds'])
        print(ticker, rsi, direction, QUANTITY)



        if (rsi <= 33 and rsi >= 14) and direction == 'buy':
            print("Buying initiated ::", ticker)
            order = auth_client.buy(product_id= ticker, order_type='market', size= QUANTITY)
            print(order)

            print(positions)

            time.sleep(1.2)
            try:
                check = order['id']
                check_order = auth_client.get_order(order_id=check)
                loger.info(order)


            except Exception as e:
                placer = auth_client.place_limit_order(product_id=ticker, size=QUANTITY, side='buy', price=price)
                checker = placer['id']
                try:
                    check_order = auth_client.get_order(order_id= checker)
                    positions.append(check_order)
                    loger.info(check_order)
                except Exception as e:
                    pass

            try:
                if check_order['status'] == 'done':
                    positions.append(check_order)
                    print('Order placed successfully')
                    print(check_order, '------- INFO!------(price)')
                    break
                else:
                    print('Order was not matched')
                    break

            except Exception as e:
                print(e)
                pass




        elif rsi >= 70 and direction == "sell":

            print("Selling initiated ::", ticker)
            #pos = auth_client.place_market_order(product_id= ticker, side= "sell", size= QUANTITY)
            pos = auth_client.sell(product_id= ticker, order_type='market', size= QUANTITY)
            print(pos)
            print(positions)
            loger.info(pos)
            time.sleep(1.2)

            try:
                check = pos['id']
                check_order = auth_client.get_order(order_id=check)
            except Exception as e:
                print(f'Unable to check order. It might be rejected. {e}')

            try:
                if check_order['status'] == 'done':
                    positions.append(check_order)
                    print('Order placed successfully')
                    print(check_order, '-------INFO! ---(price)')
                    break
                else:
                    print('Order was not matched')
                    break
            except Exception as e:
                pass

        else:
            pass


        time.sleep(5)
        with open('orders.json', 'w') as file:
            json.dump(positions, file)




if __name__ == '__main__':
    while True:

        main()
