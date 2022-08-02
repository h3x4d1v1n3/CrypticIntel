async def getcoins(self, msg):
    channel_id = msg.channel.id

    if len(self.channel_config[channel_id]['funds']) > 0:
        whitelisted_coins = '>>> '

        for coin in self.channel_config[channel_id]['funds']:
            whitelisted_coins += coin + '\n'
            if len(whitelisted_coins) > 500:
                await msg.reply(whitelisted_coins)
                whitelisted_coins = '>>> '

        if len(self.channel_config[channel_id]['funds']) % 500 > 0:
            await msg.reply(whitelisted_coins)

    else:
        await msg.reply('>>> Wallet is empty')
