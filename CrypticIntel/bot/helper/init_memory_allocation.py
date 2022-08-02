from CrypticIntel.bot.config import INITIAL_FUND

def init_memory_allocation(self, channel_id):
    # create config for channel id
    if (self.channel_config.get(channel_id) == None):
        self.channel_config[channel_id] = {}

    if (self.orders.get(channel_id) == None):
        self.orders[channel_id] = {}

    # if (self.add_by.get(channel_id) == None):
    #     self.orders[channel_id] = {}

    if (self.channel_config[channel_id].get('is_active') == None):
        self.channel_config[channel_id]['is_active'] = False

    if (self.channel_config[channel_id].get('candle_interval') == None):
        self.channel_config[channel_id]['candle_interval'] = '15m'

    # create config for funds
    if (self.channel_config[channel_id].get('funds') == None):
        self.channel_config[channel_id]['funds'] = {}

    # create config for funds
    if (self.channel_config[channel_id].get('collateral') == None):
        self.channel_config[channel_id]['collateral'] = {}

    if (self.channel_config[channel_id]['collateral'].get('USDT') == None):
        self.channel_config[channel_id]['collateral']['USDT'] = INITIAL_FUND
    
    # create config for tradetime
    if (self.channel_config[channel_id].get('tradetime') == None):
        self.channel_config[channel_id]['tradetime'] = {}

    if (self.channel_config[channel_id]['tradetime'].get('from') == None):
        self.channel_config[channel_id]['tradetime']['from'] = 0

    if (self.channel_config[channel_id]['tradetime'].get('to') == None):
        self.channel_config[channel_id]['tradetime']['to'] = 0

    