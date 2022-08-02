import technical_analysis as ta
from .helpers import *

stop_profit_percent = 2
waiting_candle_limit = 96
def no_greed(self, coin, candles, channel_id):
    ma44 = ta.SMA(candles['close'][:-1], 44)
    ma200 = ta.SMA(candles['close'][:-1], 200)

    ma44_crosses_close_over = ta.CROSSOVER(ma44, candles['close'][:-1]) 
    close_is_above_ma200 = candles['close'][-2] > ma200[-2]
    is_green_candle  = candles['close'][-2] > candles['open'][-2]

    buy_condition = ma44_crosses_close_over & close_is_above_ma200 & is_green_candle

    order = {}
    msg = ''
    if self.orders[channel_id].get(coin) is None:
        if buy_condition[-1] == 1:
            order = {
                'side' : 'buy',
                'price' : candles['close'][-1],
                'buy_at' : candles['close'][-1],
                'stop_profit' : candles['close'][-1]*(100+stop_profit_percent)/100,
                'leverage' : 1,
                'timestamp' : candles['close_time'][-1]
            }
            self.orders[channel_id][coin] = order
    else:
        order = self.orders[channel_id][coin]

        wait_to_hit_stop_profit = False
        for cur in range(1, waiting_candle_limit):
            if order['timestamp'] == candles['close_time'][-cur]:
                wait_to_hit_stop_profit = True
                break

        if not wait_to_hit_stop_profit:
            order['side'] = 'sell'
            order['price'] = candles['close'][-1]
            self.orders[channel_id].pop(coin)
        elif order['stop_profit'] <= candles['close'][-1]:
            order['side'] = 'sell'
            order['price'] = order['stop_profit']
            self.orders[channel_id].pop(coin)
        else:
            order['side'] = 'hold'
            order['price'] = candles['close'][-1]
            self.orders[channel_id][coin] = order


    return order, msg
