buying_capacity = {}
coin_min_buying_capacity = 10

def place_order(self, coin, order, channel_id):
    if buying_capacity.get(channel_id) is None:
        buying_capacity[channel_id] = {}
    if buying_capacity[channel_id].get(coin) is None:
        buying_capacity[channel_id][coin] = {'max' : self.max_buying_capacity, 'current' : 0}

    if order['side'] == 'buy':
        if self.channel_config[channel_id]['collateral'][self.collateral] >= self.min_buying_capacity:
            if buying_capacity[channel_id][coin]['max'] >= self.min_buying_capacity:

                buying_capacity[channel_id][coin]['current'] = buying_capacity[channel_id][coin]['max'] + self.channel_config[channel_id]['collateral'][self.collateral]%self.min_buying_capacity
                if buying_capacity[channel_id][coin]['current'] > self.channel_config[channel_id]['collateral'][self.collateral]:
                    buying_capacity[channel_id][coin]['current'] = buying_capacity[channel_id][coin]['max']
                if buying_capacity[channel_id][coin]['current'] > self.channel_config[channel_id]['collateral'][self.collateral]:
                    buying_capacity[channel_id][coin]['current'] = self.channel_config[channel_id]['collateral'][self.collateral]

                if buying_capacity[channel_id][coin]['current'] > buying_capacity[channel_id][coin]['max']:
                    buying_capacity[channel_id][coin]['max'] = buying_capacity[channel_id][coin]['current']

                print('investing amount - '+str(buying_capacity[channel_id][coin]['current']))
                self.channel_config[channel_id]['collateral'][self.collateral] -= buying_capacity[channel_id][coin]['current']
                self.channel_config[channel_id]['funds'][coin] = buying_capacity[channel_id][coin]['current']
                return True, self.channel_config[channel_id]['funds'][coin]
            
    # check the sell condition
    elif order['side'] == 'sell':
        if buying_capacity[channel_id][coin]['max'] < self.channel_config[channel_id]['funds'][coin]:
            buying_capacity[channel_id][coin]['max'] = self.channel_config[channel_id]['funds'][coin]
        
        sell_amount = self.channel_config[channel_id]['funds'][coin]
        self.channel_config[channel_id]['funds'][coin] = 0
        self.channel_config[channel_id]['collateral'][self.collateral] += sell_amount
        # buying_capacity[channel_id].pop(coin)
        return True, sell_amount

    elif order['side'] == 'hold':
        leverage = 1
        # try:
        if order.get('leverage') is not None:
            leverage = int(order.get('leverage'))
        # except ValueError:
        #     leverage = 1
            
        self.channel_config[channel_id]['funds'][coin] = buying_capacity[channel_id][coin]['current']*leverage*order['price']/order['buy_at']
        return True, self.channel_config[channel_id]['funds'][coin]

    return False, -1

    