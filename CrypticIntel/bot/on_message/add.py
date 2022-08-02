async def add(self, msg):
    try:
        coins = msg.content.split(' ')[1:]
        channel_id = msg.channel.id
        
        coins_info = self.binance_client.get_exchange_info()

        valid_coins = {}
        for coin_info in coins_info['symbols']:
            valid_coins[coin_info['symbol']] = True

        for coin in coins:
            is_added = False
            coin = coin.upper()
            if valid_coins.get(coin) == True:
                if self.channel_config[channel_id]['funds'].get(coin) is None:
                    self.channel_config[channel_id]['funds'][coin] = {'initial_investment':0, 'current_investment':0}
                    is_added = True
                        

            if not is_added:
                if self.channel_config[channel_id]['funds'].get(coin) is not None:
                    await msg.reply('>>> It\'s already added...')
                else:
                    await msg.reply(f">>> Did not found {msg.content.split(' ')[1]}..")
            else:
                await msg.reply('>>> '+coin+' is added to the whitelist')
                if self.add_by.get(channel_id) is not None:
                    self.add_by.pop(channel_id)
                    await msg.reply('>>> addby function is stopped')
    except IndexError:
        if self.debug:
            print('Invalid Command')
        await msg.reply('Invalid Command')
