async def clear(self, msg):
    channel_id = msg.channel.id
    if (self.channel_config.get(channel_id) is not None):
        self.channel_config.pop(channel_id)
        await msg.reply('Cleared cache')
    else:
        await msg.reply('No need to clear...')
