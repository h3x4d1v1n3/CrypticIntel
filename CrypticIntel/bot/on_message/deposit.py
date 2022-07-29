async def deposit(self, msg):
    channel_id = msg.channel.id
    try:
        cmd = msg.content.split(' ')
        fund = int(cmd[-1])
        if fund <= 0:
            raise ValueError

        self.channel_config[channel_id]['collateral']['USDT'] += fund
        await msg.reply(f">>> Added ${fund} to your wallet, you have {self.channel_config[channel_id]['collateral']['USDT']} USDT")
    except IndexError:
        if self.debug:
            print('Invalid Command')
        await msg.reply('Invalid Command')
