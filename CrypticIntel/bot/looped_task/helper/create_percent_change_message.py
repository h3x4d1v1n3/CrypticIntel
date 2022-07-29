def create_percent_change_message(changed_val, previous_val):
    change_per = changed_val*100/previous_val - 100
    if change_per > 0:
        msg = f'{abs(round(change_per, 2))}% up'
    elif change_per < 0:
        msg = f'{abs(round(change_per, 2))}% down'
    else:
        msg = 'no change'

    return msg
