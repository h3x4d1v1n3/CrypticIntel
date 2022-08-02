async def addby(self, msg):
    try:
        channel_id = msg.channel.id

        cmd = msg.content.split(' ')[1:]
        if len(cmd) == 1:
            add_by = cmd[0]
            limit = -1
        if len(cmd) == 2:
            add_by = cmd[0]
            limit = int(cmd[1])
        else:
            raise ValueError

        self.add_by[channel_id] = {'add_by' : add_by, 'limit':limit, 'is_cached':False}
        await msg.reply(f">>> Adding coins by {self.add_by[channel_id]['add_by']}")

    except (IndexError, ValueError):
        if self.debug:
            print('Invalid Command')
        await msg.reply('Invalid Command')
