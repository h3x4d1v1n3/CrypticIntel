async def setinterval(self, msg):
    try:
        valid_intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '1w', '3d' ]
        interval = msg.content.split(' ')[1]
        channel_id = msg.channel.id
        if interval in valid_intervals:
            self.channel_config[channel_id]['candle_interval'] = interval
            await msg.reply(f'candlestick interval set to {interval}')
        else:
            await msg.reply('Invalid candlestick interval')

    except IndexError:
        if self.debug:
            print('Invalid Command')
        await msg.reply('Invalid Command')