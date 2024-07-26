import json 

users = []

def add_user(username):
    # current_users = []
    # with open('db/users.json', 'r') as users:
    #     current_users = json.load(users)
    if username not in users:
        users.append(username)
        # with open('db/users.json', 'w') as users:
        #     users.write(json.dumps(current_users))
        return True
    else:
        return False

def remove_user(username):
    # current_users = []
    # with open('db/users.json', 'r') as users:
    #     current_users = json.load(users)
    if username in users:
        users.remove(username)
        # with open('db/users.json', 'w') as users:
        #     users.write(json.dumps(current_users))

def get_users():
    # users = []
    # with open('db/users.json', 'r') as usersfile:
    #     users = json.load(usersfile)
    return users
