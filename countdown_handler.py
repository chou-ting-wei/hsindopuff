import datetime, json, sys
sys.set_int_max_str_digits(0)

with open('data.json', mode='r', encoding='utf8') as jfile:
    data = json.load(jfile)

def get_today():
    today = datetime.date.today()
    # today = datetime.datetime.today() + datetime.timedelta(hours = 6)
    return today.strftime("%Y/%m/%d")

def get_now():
    now = datetime.datetime.now()
    # now = datetime.datetime.now() + datetime.timedelta(hours = 6)
    return now.strftime("%Y/%m/%d %H:%M:%S")

def find_countdown(event):
    countdown_index = 0 
    for i in range(len(data['countdown_list'])):
        if data['countdown_list'][i]['event'] == event:
            countdown_index = i + 1
    if countdown_index > 0:
        return True
    else:
        return False

def get_countdown():
    today = datetime.date.today()
    # today = datetime.datetime.today() + datetime.timedelta(hours = 6)
    # too = datetime.date(today.year, today.month, today.day)
    ret_message = ""
    for i in range(len(data['countdown_list'])):
        target_day = datetime.date(data['countdown_list'][i]['year'], data['countdown_list'][i]['month'], data['countdown_list'][i]['day'])
        difference = target_day - today
        # difference = target_day - too
        if difference.days == 0:
            ret_message += ("今天是 `" + data['countdown_list'][i]['event'] + "`！\n")
            if str(data['countdown_list'][i]['add']) != 'NULL':
                ret_message += ("可愛的 hsindopuff 祝大家" + data['countdown_list'][i]['add'] + " :tada:\n")
        if str(data['countdown_list'][i]['view']) == 'false':
            continue
        if difference.days < 0:
            if abs(difference.days) < int(data['countdown_list'][i]['last']):
                ret_message += ("今天是 `" + data['countdown_list'][i]['event'] + "`！\n")
        if difference.days > 0:
            ret_message += ("\n距離 `" + data['countdown_list'][i]['event'] + "` 還剩下 `" + str(difference.days) + "` 天")
    ret_message += "\n<:rip:1023630791172968620>"
    return ret_message

def get_countdown_list(permission):
    ret_message = ""
    for i in range(len(data['countdown_list'])):
        if not permission:
            if data['countdown_list'][i]['view'] == 'false':
                continue
        ret_month = str(data['countdown_list'][i]['month'])
        ret_day = str(data['countdown_list'][i]['day'])
        if int(data['countdown_list'][i]['month']) < 10:
            ret_month = "0" + str(data['countdown_list'][i]['month'])
        if int(data['countdown_list'][i]['day']) < 10:
            ret_day = "0" + str(data['countdown_list'][i]['day'])
        ret_message +=  ("`" + str(data['countdown_list'][i]['year']) + "`/`" + ret_month + "`/`" + ret_day + "` `" + str(data['countdown_list'][i]['event']) + "`")
        if permission:
            ret_message += " `" + str(data['countdown_list'][i]['add']) + "`"
            if data['countdown_list'][i]['view'] == 'false':
                ret_message += " `#`"
        ret_message += '\n'
    return ret_message

def add_countdown(permission, view, event, year, month, day, last, add):
    if permission:
        if find_countdown(event):
            return "Countdown already exists!"
        with open('data.json', mode = 'w', encoding = 'utf8') as jfile:
            data['countdown_list'].append({'view':view, 'event':event, 'year':int(year), 'month':int(month), 'day':int(day), 'last':int(last), 'add':add, 'key':int(year) * 10000 + int(month) * 100 + int(day)})
            data['countdown_list'].sort(key = lambda x : int(x['key']))
            json.dump(data, jfile, indent = 4)
        return "Countdown added successfully!"
    else:
        return "You do not have enough permission to do this."
    
def delete_countdown(permission, event):
    if permission:
        countdown_index = 0 
        for i in range(len(data['countdown_list'])):
            if data['countdown_list'][i]['event'] == event:
                countdown_index = i + 1
        if countdown_index == 0:
            return "Countdown does not exist!"
        else:
            with open('data.json', mode = 'w', encoding = 'utf8') as jfile:
                data['countdown_list'].pop(countdown_index - 1)
                json.dump(data, jfile, indent = 4)
            return "Countdown deleted successfully!"
    else:
        return "You do not have enough permission to do this."