import time

def get_candles(binance_client, coin, interval, limit):
    candles = []
    for _ in range(10):
        # try:
        candles = binance_client.get_klines(symbol=coin, interval=interval, limit=limit)
        break
        # except Exception as e:
        #     print(e)
        #     time.sleep(2)

    # parse data
    open_time = []
    open_price = []
    high_price = []
    low_price = []
    close_price = []
    volume = []
    close_time = []

    total_candles = len(candles)
    for i in range(total_candles):
        open_time.append(candles[i][0])
        open_price.append(float(candles[i][1]))
        high_price.append(float(candles[i][2]))
        low_price.append(float(candles[i][3]))
        close_price.append(float(candles[i][4]))
        volume.append(float(candles[i][5]))
        close_time.append(candles[i][6])

    return { 'open_time': open_time, 'open':open_price, 'high':high_price, 'low':low_price, 'close':close_price, 'volume':volume, 'close_time':close_time }