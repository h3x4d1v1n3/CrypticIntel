import technical_analysis as ta

def ma_cross_remix(self, coin, candles, channel_id):
    slow_ma = ta.EMA(candles['close'][:-1], 26)
    fast_ma = ta.EMA(candles['close'][:-1], 9)
    rsi = ta.RSI(candles['close'][:-1], 14)
    plus_di, minus_di, _ = ta.DMI(candles['high'][:-1], candles['low'][:-1], candles['close'][:-1], 14)

    buy_condition = (fast_ma > slow_ma) & (plus_di > minus_di) & (rsi < 60)
    sell_condition = (fast_ma < slow_ma) | (rsi > 70)

    order = {}
    msg = ''
    if self.orders[channel_id].get(coin) is None:
        if buy_condition[-1] == 1:
            order = {
                'side' : 'buy',
                'price' : candles['close'][-1],
                'buy_at' : candles['close'][-1],
                'leverage' : 1,
                'timestamp' : candles['close_time'][-1]
            }
            self.orders[channel_id][coin] = order
    else:
        if sell_condition[-1] == 1:
            order = self.orders[channel_id][coin]
            order['side'] = 'sell'
            order['price'] = candles['close'][-1]
            self.orders[channel_id].pop(coin)
        else:
            self.orders[channel_id][coin]['side'] = 'hold'
            self.orders[channel_id][coin]['price'] = candles['close'][-1]
            order = self.orders[channel_id][coin]

    
    return order, msg
