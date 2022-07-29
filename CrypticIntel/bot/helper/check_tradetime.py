import datetime

def check_tradetime(trade_from, trade_to):
    current_time = datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)
    current_time = current_time.hour*100+current_time.minute

    if trade_from < trade_to:
        if trade_from <= current_time and current_time <= trade_to:
            return True
    if trade_from > trade_to:
        if (trade_from <= current_time  and current_time <= 1159) or (0 <= current_time and current_time <= trade_to):
            return True
    else:
        return True

    return False
    
    