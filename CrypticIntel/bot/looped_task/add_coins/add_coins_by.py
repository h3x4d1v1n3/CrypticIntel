from CrypticIntel.bot.helper import load_functions_from
from .by import *

def add_coins_by(self, channel_id):
    add_coin_by_functions = load_functions_from(self.ADD_COINS_BY_PATH)
    add_by = self.add_by[channel_id]['add_by'].lower()
    limit = self.add_by[channel_id]['limit']
    print('adding coins by')
    print(add_by)
    if add_by in add_coin_by_functions:
        coins = eval(add_by)(self, limit)
        for coin in coins:
            if self.channel_config[channel_id]['funds'].get(coin) is None:
                self.channel_config[channel_id]['funds'][coin] = {'initial_investment':0, 'current_investment':0}
    else:
        print('invalid addby function')