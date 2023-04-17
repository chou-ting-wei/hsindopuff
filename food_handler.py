import datetime, json, random

data = {}
with open('data.json', mode='r', encoding='utf8') as jfile:
    data = json.load(jfile)
    
def get_food():
    return data['food_list'][random.randint(0, int(len(data['food_list']) - 1))]

def get_food_list():
    ret_message = ""
    for i in range(len(data['food_list'])):
        if (i + 1) < 10:
            ret_message += "`#0" + str(i + 1) + "`  `"
        else:
            ret_message += "`#" + str(i + 1) + "`  `"
        ret_message += (data['food_list'][i] + "`\n")
    return ret_message