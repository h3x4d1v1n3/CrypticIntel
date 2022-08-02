"""
command : tradetime 15:00 15:30
"""
async def tradetime(self, msg):
    channel_id = msg.channel.id
    try:
        tradetime_cmd = msg.content.split(' ')
        if len(tradetime_cmd) == 3:
            trade_from = [ int(tradetime_from) for tradetime_from in tradetime_cmd[1].split(':') ]
            trade_to   = [ int(tradetime_to)   for tradetime_to   in tradetime_cmd[2].split(':') ]
            self.channel_config[channel_id]['tradetime']['from'] = trade_from[0]*100+trade_from[1]
            self.channel_config[channel_id]['tradetime']['to']   = trade_to[0]*100+trade_to[1]
            await msg.reply(f'>>> Trading will start from {tradetime_cmd[1]} to {tradetime_cmd[2]}')
        else:
            raise ValueError
    except IndexError:
        if self.debug:
            print('Invalid Tradetime Command')
        await msg.reply('Invalid Tradetime Command')
