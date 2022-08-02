async def withdraw(self, msg):
    channel_id = msg.channel.id
    try:
        cmd = msg.content.split(' ')
        fund = float(cmd[-1])
        if fund <= 0:
            raise ValueError

        if self.channel_config[channel_id]['collateral']['USDT'] < fund:
            self.channel_config[channel_id]['collateral']['USDT'] = 0
            await msg.reply('>>> Withdrawn all balance from your wallet')
        else:
            self.channel_config[channel_id]['collateral']['USDT'] -= fund
            await msg.reply(f">>> Withdrawn ${fund} from your wallet, you have {self.channel_config[channel_id]['collateral']['USDT']} USDT")
    except IndexError:
        if self.debug:
            print('Invalid Command')
        await msg.reply('Invalid Command')
