async def activate(self, msg):
    channel_id = msg.channel.id
    if msg.content.lower() == 'activate':
        self.channel_config[channel_id]['is_active'] = True
        await msg.reply('The Strategy is Activated')