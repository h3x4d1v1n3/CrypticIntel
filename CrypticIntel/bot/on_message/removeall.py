import copy
from CrypticIntel.bot.looped_task.place_order import place_order
from CrypticIntel.bot.looped_task import send_message
from CrypticIntel.bot.helper import set_lock, release_lock

async def removeall(self, msg):
    try:
        await msg.reply(f'>>> Processing...')

        collateral = msg.content.split(' ')[1].upper()
        channel_id = msg.channel.id

        channel_config =  copy.deepcopy(self.channel_config)
        self.channel_config[channel_id]['funds'] = {}

        is_removed = False
        print(channel_config[channel_id]['funds'])
        
        for coin in list(channel_config[channel_id]['funds']):
            if collateral == coin[-len(collateral):] and (channel_config[channel_id]['funds'].get(coin) is not None and channel_config[channel_id]['funds'][coin]['initial_investment'] != 0):
                order = {
                    'side' : 'sell',
                }
                # get confirmation and invested amount, (channel_config is not required for that)
                order_is_placed, amount, channel_config = place_order(coin, order, channel_id, channel_config, collateral, self.min_buying_capacity, self.leverage)
                # if order is placed send msg
                if order_is_placed:
                    print(f'order is placed')
                    await send_message(self, coin, order, channel_id, amount, msg)

            if self.orders[channel_id].get(coin) is not None:
                self.orders[channel_id].pop(coin)

            is_removed = True

        if not is_removed:
            await msg.reply(f">>> {msg.content.split(' ')[1]} is an invalid collateral...")
        else:
            self.channel_config[channel_id]['collateral'][collateral] = channel_config[channel_id]['collateral'][collateral]
            await msg.reply(f'>>> All {collateral} coins are removed from the whitelist')
            if self.add_by.get(channel_id) is not None:
                self.add_by.pop(channel_id)
                await msg.reply('>>> addby function is stopped')
    except IndexError:
        if self.debug:
            print('Invalid Command')
        await msg.reply('Invalid Command')
  
