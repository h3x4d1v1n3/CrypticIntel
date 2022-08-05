from CrypticIntel.bot.on_message.deposit import deposit

# bought_at

def place_order(coin, order, channel_id, channel_config, collateral, min_buying_capacity, leverage=1):
    deposited_fund = channel_config[channel_id]['collateral'][collateral]
    investment_fund = channel_config[channel_id]['funds'][coin]['current_investment']
    buying_capacity_percent = 10
    # min_buying_capacity = 10   # not dynamic
    # self.leverage = 1
    if order.get('leverage') is not None:
        leverage = int(order.get('leverage'))

    # buy condition
    if order['side'] == 'buy':
        investment_fund = deposited_fund*leverage*buying_capacity_percent/100
        # not a dynamic check - not depending on rules of binance (has static min_buying_capacity)
        if investment_fund > min_buying_capacity:
            channel_config[channel_id]['funds'][coin] = {}
            channel_config[channel_id]['funds'][coin]['initial_investment'] = investment_fund
            channel_config[channel_id]['funds'][coin]['current_investment'] = investment_fund
            channel_config[channel_id]['collateral'][collateral] -= investment_fund
            return True, investment_fund, channel_config
        elif deposited_fund > min_buying_capacity:
            channel_config[channel_id]['funds'][coin] = {}
            channel_config[channel_id]['funds'][coin]['initial_investment'] = min_buying_capacity
            channel_config[channel_id]['funds'][coin]['current_investment'] = min_buying_capacity
            channel_config[channel_id]['collateral'][collateral] -= min_buying_capacity
            return True, min_buying_capacity, channel_config
    # sell condition
    elif order['side'] == 'sell':
        channel_config[channel_id]['collateral'][collateral] += investment_fund
        channel_config[channel_id]['funds'][coin]['initial_investment'] = 0
        channel_config[channel_id]['funds'][coin]['current_investment'] = 0
        return True, investment_fund, channel_config
    # hold condition
    elif order['side'] == 'hold':
        channel_config[channel_id]['funds'][coin]['current_investment'] = channel_config[channel_id]['funds'][coin]['initial_investment']*order['price']/order['buy_at']
        return True, channel_config[channel_id]['funds'][coin]['current_investment'], channel_config

    return False, -1, channel_config

    