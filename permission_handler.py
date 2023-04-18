import json

with open('data.json', mode='r', encoding='utf8') as jfile:
    data = json.load(jfile)
    
def find_permission(author):
    permission_index = 0 
    for i in range(len(data['permission_list'])):
        if data['permission_list'][i] == author:
            permission_index = i + 1
    if permission_index > 0:
        return True
    else:
        return False

def add_permission(permission, id):
    if permission:
        if find_permission(str(id)):
            return "Admin already exists!"
        else:
            with open('data.json', mode = 'w', encoding = 'utf8') as jfile:
                data['permission_list'].append(str(id))
                json.dump(data, jfile, indent = 4)  
            return 'Admin added successfully!'
    else:
        return "You do not have enough permission to do this."
    
def delete_permission(permission, id):
    if str(id) == "764407051791106069":
        return "You can not remove this admin."
    if permission:
        permission_index = 0 
        for i in range(len(data['permission_list'])):
            if data['permission_list'][i] == str(id):
                permission_index = i + 1
        if permission_index == 0:
            return "Admin does not exist!"
        else:
            with open('data.json', mode = 'w', encoding = 'utf8') as jfile:
                data['permission_list'].pop(permission_index - 1)
                json.dump(data, jfile, indent = 4)
            return "Admin deleted successfully!"
    else:
        return "You do not have enough permission to do this."