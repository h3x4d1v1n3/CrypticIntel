async def addall(self, msg):
    """Adds all the coins of given collateral."""
    print(msg)
    try:
        collaterals = ['USDT', 'BTC']
        collateral = msg.content.split(' ')[1].upper()
        channel_id = msg.channel.id
        coins_info = self.binance_client.get_exchange_info()

        is_added = False
        for coin_info in coins_info['symbols']:
            if collateral == coin_info['symbol'][-len(collateral):] and collateral in collaterals:
                if self.channel_config[channel_id]['funds'].get(coin_info['symbol']) is None:
                    self.channel_config[channel_id]['funds'][coin_info['symbol']] = 0
                    is_added = True

        if not is_added:
            await msg.reply(f">>> {msg.content.split(' ')[1]} collateral is not added...")
        else:
            await msg.reply(f'>>> All {collateral} coins are added to the whitelist')
            if self.add_by.get(channel_id) is not None:
                self.add_by.pop(channel_id)
                await msg.reply('>>> addby function is stopped')
    except IndexError:
        if self.debug:
            print('Invalid Command')
        await msg.reply('Invalid Command')
