import datetime, json

data = {}
with open('data.json', mode='r', encoding='utf8') as jfile:
    data = json.load(jfile)

def get_today():
    today = datetime.date.today()
    return str(today)

def get_now():
    now = datetime.datetime.now()
    return now.strftime("%Y/%m/%d %H:%M:%S")

def get_countdown():
    today = datetime.date.today()
    ret_message = ""
    for i in range(len(data['countdown_list'])):
        target_day = datetime.date(data['countdown_list'][i]['year'], data['countdown_list'][i]['month'], data['countdown_list'][i]['day'])
        difference = target_day - today
        if difference.days == 0:
            ret_message += ("今天是 `" + data['countdown_list'][i]['event'] + "`！\n")
            if data['countdown_list'][i]['add'] != '':
                ret_message += ("可愛的 hsindopuff 祝大家" + data['countdown_list'][i]['add'] + " :tada:\n")
        if data['countdown_list'][i]['view'] == 'false':
            continue
        if difference.days < 0:
            if abs(difference.days) < int(data['countdown_list'][i]['last']):
                ret_message += ("今天是 `" + data['countdown_list'][i]['event'] + "`！\n")
        if difference.days > 0:
            ret_message += ("\n距離 `" + data['countdown_list'][i]['event'] + "` 還剩下 `" + str(difference.days) + "` 天")
    ret_message += "\n<:rip:900761668542414879>"
    return ret_message

def get_countdown_list():
    ret_message = ""
    for i in range(len(data['countdown_list'])):
        if data['countdown_list'][i]['view'] == 'false':
            continue
        ret_month = str(data['countdown_list'][i]['month'])
        ret_day = str(data['countdown_list'][i]['day'])
        if(data['countdown_list'][i]['month']) < 10:
            ret_month = "0" + str(data['countdown_list'][i]['month'])
        if(data['countdown_list'][i]['day']) < 10:
            ret_day = "0" + str(data['countdown_list'][i]['day'])
        ret_message +=  ("`" + str(data['countdown_list'][i]['year']) + "`/`" + ret_month + "`/`" + ret_day + "` `" + str(data['countdown_list'][i]['event']) + "`\n")
    return ret_message