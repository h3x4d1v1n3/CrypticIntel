async def deactivate(self, msg):
    channel_id = msg.channel.id
    if msg.content.lower() == 'deactivate':
        self.channel_config[channel_id]['is_active'] = False
        await msg.reply('The Strategy is Deactivated')
