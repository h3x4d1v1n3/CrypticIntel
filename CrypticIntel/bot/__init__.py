import discord
from discord.ext import tasks
import asyncio
import datetime
import binance

from CrypticIntel.channels import *
from .config import BLACKLISTED_COINS

from .on_message import *
from .looped_task import *
from .helper import *

class CrypticIntel(discord.Client):
    """This is class docstring"""
    def __init__(self, debug):
        intents=discord.Intents.default()
        intents.members = True
        super().__init__(intents=discord.Intents.all())
        self.binance_client = binance.Client()
        self.channel_config = {}
        self.debug = debug
        self.__ON_MESSAGES_PATH = './CrypticIntel/bot/on_message'
        self.__CHANNELS_PATH = './CrypticIntel/channels'
        self.ADD_COINS_BY_PATH = './CrypticIntel/bot/looped_task/add_coins/by'
        self.orders = {}
        self.collateral = 'USDT'
        self.min_buying_capacity = 10
        self.max_buying_capacity = 20
        self.add_by = {}

        self.blacklisted_coins = []
        for coins in BLACKLISTED_COINS:
            self.blacklisted_coins.append(coins+self.collateral)

    async def on_ready(self):
        """Interprate once bot get ready"""
        print('test init')
        # change name of functions later
        self.looped_task()
        self.looped_task2()
        if self.debug:
            print('\n[0_0] Initialized. \n')

    def looped_task2(self):
        # @tasks.loop(minutes=2)
        @tasks.loop(hours=24)
        async def loop_task():
            # set cache to false to fetch new data every 24hrs
            print('clearing cache')
            for channel_id in self.add_by:
                self.add_by[channel_id]['is_cached'] = False

            # await asyncio.sleep(24*60*60)

        loop_task.start()

    def looped_task(self):
        """This is a looped task"""
        @tasks.loop(seconds=5.0)
        async def loop_task():
            current_time = datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)
            print(f'\nlooping through the loop at {current_time.day}/{current_time.month} - {current_time.hour}:{current_time.minute}:{current_time.second}\n')
           
            # loop to check if addby rule is used? and to add coins by given condition like marketcap, volume, change and cache for 24hrs
            for channel_id in self.add_by:
                if self.add_by[channel_id]['is_cached'] is False:
                    add_coins_by(self, channel_id)
                    self.add_by[channel_id]['is_cached'] = True

            # load name of channels (strategies)
            channels = load_functions_from(self.__CHANNELS_PATH)
            coins_info = self.binance_client.get_exchange_info()

            # fetch valid coins (used hashmap method to store)
            valid_coins = {}
            for coin_info in coins_info['symbols']:
                valid_coins[coin_info['symbol']] = True

            # iterate through channel and coins
            for channel_id in set(self.channel_config):
                if (self.channel_config[channel_id]['is_active'] is False):
                    continue
                
                channel = self.get_channel(channel_id)
                print()
                for coin in set(self.channel_config[channel_id]['funds']):
                    print('--', end='')
                    # added coin should be valid one (final check)
                    if valid_coins.get(coin) is not True and self.channel_config[channel_id]['funds'].get(coin) is not None:
                        self.channel_config[channel_id]['funds'].pop(coin)
                        continue
                    # print(coin)
                    # if coin does not belong to channel or coin or collateral does not have minimum fund to tread then exit loop
                    if self.channel_config[channel_id]['funds'].get(coin) is None or str(channel) not in channels:
                        continue
                    # if usdt is less than buying capacity and check for whether coin is already bought or not if not exit else proceed to check hold or sell condition
                    # check this - seems good
                    if self.channel_config[channel_id]['collateral'][self.collateral] < self.min_buying_capacity and self.orders[channel_id].get(coin) is None:
                        continue
                    if coin in self.blacklisted_coins and self.channel_config[channel_id]['funds'].get(coin) is not None:
                        self.channel_config[channel_id]['funds'].pop(coin)
                        continue

                    # fetch candlestick data
                    candles = get_candles(self.binance_client, coin, self.channel_config[channel_id]['candle_interval'], 1000)
                    # apply strategies
                    order, msg = eval(str(channel))(self, coin, candles, channel_id)
                    if order != {}:
                        print('\n'+coin + ' ' + str(channel)+' '+self.channel_config[channel_id]['candle_interval'])
                        print(order)
                        # need to work on placing real orders
                        if check_tradetime(self.channel_config[channel_id]['tradetime']['from'], self.channel_config[channel_id]['tradetime']['to']) or (order['side'] == 'sell' or order['side'] == 'hold'):
                            order_is_placed, amount = place_order(self, coin, order, channel_id)

                            if order_is_placed:
                                print(f'order placed - {order_is_placed}')
                                print('sending msg')
                                # change name from send message to something else we are creating threads
                                await send_message(self, coin, order, channel_id, amount, msg)
                            else:
                                print('removing unplaced order')
                                if self.orders[channel_id].get(coin) is not None:
                                    self.orders[channel_id].pop(coin)
                    # sleep this thread to check other thread
                    await asyncio.sleep(0.01)
                # send total invested and non invested fund
                await send_balance_sheet(self, channel_id)
                # sleep this thread to check other thread
                await asyncio.sleep(0.1)

            # await asyncio.sleep(1)

        loop_task.start()

    async def on_message(self, msg):
        """Check for message(commands) and execute"""
        await self.wait_until_ready()
        if msg.author == self.user:
            return
        print(msg)

        # allocate configuration file for specific channel
        if (msg.channel.id not in self.channel_config):
            init_memory_allocation(self, msg.channel.id)

        # load functions from ./on_message folder
        functions = load_functions_from(self.__ON_MESSAGES_PATH)
        print(functions)
        print(msg.content)
        # execute loaded functions
        for function in functions:
            if msg.content.split(' ')[0].lower() == function:
                await eval(function)(self, msg)
                break

        if self.debug:
            print(self.channel_config)
