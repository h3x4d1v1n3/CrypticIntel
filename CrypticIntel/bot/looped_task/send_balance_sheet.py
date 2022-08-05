import discord

balance_sheet_message = {}
async def send_balance_sheet(self, channel_id):
    
    if balance_sheet_message.get(channel_id) is None:
        balance_sheet_message[channel_id] = {}
    elif balance_sheet_message[channel_id].get('message') is not None:
        # try:
        if len(self.channel_config[channel_id]['funds']) == 0:
            return
            
        await balance_sheet_message[channel_id]['message'].delete()
        balance_sheet_message[channel_id]['message']=None
        # except discord.errors.NotFound:
        #     pass

    balance = 0
    balance_sheet = '>>> '
    for collateral in list(self.channel_config[channel_id]['collateral']):
        if self.channel_config[channel_id]['collateral'][collateral] > 0:
            balance += self.channel_config[channel_id]['collateral'][collateral]
            balance_sheet += f"{collateral} : {round(self.channel_config[channel_id]['collateral'][collateral],2)}\n"

    for coin in list(self.channel_config[channel_id]['funds']):
        if self.channel_config[channel_id]['funds'][coin].get('current_investment') is not None and self.channel_config[channel_id]['funds'][coin]['current_investment'] > 0:
            balance += self.channel_config[channel_id]['funds'][coin]['current_investment']
            balance_sheet += f"{coin} : {round(self.channel_config[channel_id]['funds'][coin]['current_investment'], 2)}\n"

    if balance == 0:
        return

    embed_var = discord.Embed(title=f"Total Fund is ${round(balance, 2)}")
    embed_var.color = 0xffff00
    embed_var.description = balance_sheet

    channel = self.get_channel(channel_id)
    if channel_id is not None:
        message = await channel.send(embed=embed_var)
        balance_sheet_message[channel_id]['message'] = message
    else:
        print('=()= bug =()=')
        print(channel_id)
        print()
        print(self.channel_config)
        exit()