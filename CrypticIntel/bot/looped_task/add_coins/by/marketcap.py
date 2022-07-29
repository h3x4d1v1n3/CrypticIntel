from pycoingecko import CoinGeckoAPI

def marketcap(self, limit):
    coin_gecko = CoinGeckoAPI()

    data_set = []
    if limit == -1:
        data_set = coin_gecko.get_coins_markets('usd', order='market_cap_desc')
    else:
        pages = limit//250+1
        for page in range(pages):
            per_page = limit%250
            fetched_data = coin_gecko.get_coins_markets('usd', order='market_cap_desc', per_page=per_page, page=page)
            data_set.extend(fetched_data)
            limit -= per_page

    coins = []
    for data in data_set:
        coins.append(data['symbol'].upper()+self.collateral)
    
    print(f'\nBelow {len(coins)} coins will be added\n')
    print(coins)
    print('\n')
    return coins
