from CrypticIntel.bot.looped_task.place_order import place_order

async def remove(self, msg):
    try:
        coin = msg.content.split(' ')[1].upper()
        channel_id = msg.channel.id

        if coin in self.channel_config[channel_id]['funds']:
            order = {
                'side' : 'sell',
            }
            order_is_placed, _ = place_order(self, coin, order, channel_id)
            if order_is_placed:
                if self.orders[channel_id].get(coin) is not None:
                    self.orders[channel_id].pop(coin)

                self.channel_config[channel_id]['funds'].pop(coin)
                await msg.reply('>>> '+coin+' is removed from the whitelist')

                if self.add_by.get(channel_id) is not None:
                    self.add_by.pop(channel_id)
                    await msg.reply('>>> addby function is stopped')
                
        else:
            await msg.reply(f">>> Did not found {msg.content.split(' ')[1]}...")
    except IndexError:
        if self.debug:
            print('Invalid Command')
        await msg.reply('Invalid Command')
