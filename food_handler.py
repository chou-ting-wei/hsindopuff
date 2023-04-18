import json, random

data = {}
with open('data.json', mode='r', encoding='utf8') as jfile:
    data = json.load(jfile)
    
def find_food(restaurant):
    food_index = 0 
    for i in range(len(data['food_list'])):
        if data['food_list'][i] == restaurant:
            food_index = i + 1
    if food_index > 0:
        return True
    else:
        return False
    
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

def add_food(permission, restaurant):
    if permission:
        if find_food(str(restaurant)):
            return "Food already exists!"
        else:
            with open('data.json', mode = 'w', encoding = 'utf8') as jfile:
                data['food_list'].append(str(restaurant))
                json.dump(data, jfile, indent = 3)  
            return 'Food added successfully!'
    else:
        return "You do not have enough permission to do this."
    
def delete_food(permission, restaurant):
    if permission:
        food_index = 0 
        for i in range(len(data['food_list'])):
            if data['food_list'][i] == str(restaurant):
                food_index = i + 1
        if food_index == 0:
            return "Food does not exist!"
        else:
            with open('data.json', mode = 'w', encoding = 'utf8') as jfile:
                data['food_list'].pop(food_index - 1)
                json.dump(data, jfile, indent = 3)
            return "Food deleted successfully!"
    else:
        return "You do not have enough permission to do this."