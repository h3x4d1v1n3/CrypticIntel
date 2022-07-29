from .helper import create_percent_change_message 
import discord

discord_threads = {}
async def send_message(self, coin, order, channel_id, amount=0, msg=''):
    print(coin + ' ' + order['side'])

    if discord_threads.get(channel_id) is None:
        discord_threads[channel_id] = {}

    if order['side'] == 'buy':
        channel = self.get_channel(channel_id)

        buy_msg = discord.Embed(title=coin)
        buy_msg.color = 0xFF4500

        if discord_threads[channel_id].get(coin) is None:
            message = await channel.send(embed=buy_msg)
            thread = await channel.create_thread(name=coin, message=message, auto_archive_duration=60)
            discord_threads[channel_id][coin] = {'main_thread':thread, 'hold_msg':None}
        else:
            discord_threads[channel_id][coin]['main_thread'].archived = False
            thread = discord_threads[channel_id][coin]['main_thread']
            discord_threads[channel_id][coin]['hold_msg'] = None

        status_msg = discord.Embed(title='Order Details')
        status_msg.description = f">>> Bought at : ${order['buy_at']}\nInvested amount : ${round(self.channel_config[channel_id]['funds'][coin], 2)}"
        status_msg.color = 0x39ff14

        print(discord_threads[channel_id][coin])
        # try:
        await thread.send(embed=status_msg)
        # except DiscordServerError as exception:
        #     print('server error - '+exception)
    else:
        coin_thread = discord_threads[channel_id][coin]
        coin_thread['main_thread'].archived = False

        # try:
        if discord_threads[channel_id][coin].get('hold_msg') is not None:
            await coin_thread['hold_msg'].delete()
            discord_threads[channel_id][coin]['hold_msg'] = None
        # except (discord.errors.NotFound, KeyError) as e:
        #     print(e)
        #     # exit()
        # finally:
        #     discord_threads[channel_id][coin]['hold_msg'] = None

        embed_var = discord.Embed(title=f"Status")
        msg = f">>> Market price : ${order['price']}\nCurrent amount : ${round(amount, 2)}\nChange : {create_percent_change_message(order['price'], order['buy_at'])}"
        embed_var.description = msg

        if order['side'] == 'sell':
            embed_var.color = 0xff0000
            await coin_thread['main_thread'].send(embed=embed_var)
            print(discord_threads[channel_id][coin])
            discord_threads[channel_id][coin]['hold_msg'] = None
            # discord_threads[channel_id].pop(coin)
        elif order['side'] == 'hold':
            embed_var.color = 0x00ffff
            message = await coin_thread['main_thread'].send(embed=embed_var)
            discord_threads[channel_id][coin]['hold_msg'] = message

            print(discord_threads[channel_id][coin])