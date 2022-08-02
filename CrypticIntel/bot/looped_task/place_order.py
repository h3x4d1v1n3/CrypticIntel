from CrypticIntel.bot.on_message.deposit import deposit

# bought_at

def place_order(self, coin, order, channel_id):
    deposited_fund = self.channel_config[channel_id]['collateral'][self.collateral]
    investment_fund = self.channel_config[channel_id]['funds'][coin]['current_investment']
    buying_capacity_percent = 10
    # min_buying_capacity = 10   # not dynamic
    # self.leverage = 1
    if order.get('leverage') is not None:
        self.leverage = int(order.get('leverage'))

    # buy condition
    if order['side'] == 'buy':
        investment_fund = deposited_fund*self.leverage*buying_capacity_percent/100
        # not a dynamic check - not depending on rules of binance (has static min_buying_capacity)
        if investment_fund > self.min_buying_capacity:
            self.channel_config[channel_id]['funds'][coin] = {}
            self.channel_config[channel_id]['funds'][coin]['initial_investment'] = investment_fund
            self.channel_config[channel_id]['funds'][coin]['current_investment'] = investment_fund
            self.channel_config[channel_id]['collateral'][self.collateral] -= investment_fund
            return True, investment_fund
        else:
            self.channel_config[channel_id]['funds'][coin] = {}
            self.channel_config[channel_id]['funds'][coin]['initial_investment'] = self.min_buying_capacity
            self.channel_config[channel_id]['funds'][coin]['current_investment'] = self.min_buying_capacity
            self.channel_config[channel_id]['collateral'][self.collateral] -= self.min_buying_capacity
            return True, self.min_buying_capacity
    # sell condition
    elif order['side'] == 'sell':
        self.channel_config[channel_id]['collateral'][self.collateral] += investment_fund
        self.channel_config[channel_id]['funds'][coin]['initial_investment'] = 0
        self.channel_config[channel_id]['funds'][coin]['current_investment'] = 0
        return True, investment_fund
    # hold condition
    elif order['side'] == 'hold':
        self.channel_config[channel_id]['funds'][coin]['current_investment'] = self.channel_config[channel_id]['funds'][coin]['initial_investment']*order['price']/order['buy_at']
        return True, self.channel_config[channel_id]['funds'][coin]['current_investment']

    return False, -1

    