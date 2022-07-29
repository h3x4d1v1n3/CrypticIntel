from CrypticIntel.bot.looped_task.place_order import place_order

async def removeall(self, msg):
    try:
        collateral = msg.content.split(' ')[1].upper()
        channel_id = msg.channel.id

        is_removed = False

        for coin in list(self.channel_config[channel_id]['funds']):
            if collateral == coin[-len(collateral):]:
                order = {
                    'side' : 'sell',
                }
                place_order(self, coin, order, channel_id)
                self.channel_config[channel_id]['funds'].pop(coin)
                is_removed = True
                if self.orders[channel_id].get(coin) is not None:
                    self.orders[channel_id].pop(coin)


        if not is_removed:
            await msg.reply(f">>> {msg.content.split(' ')[1]} is an invalid collateral...")
        else:
            await msg.reply(f'>>> All {collateral} coins are removed from the whitelist')
            if self.add_by.get(channel_id) is not None:
                self.add_by.pop(channel_id)
                await msg.reply('>>> addby function is stopped')
    except IndexError:
        if self.debug:
            print('Invalid Command')
        await msg.reply('Invalid Command')
