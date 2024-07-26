import json 

users = []

def add_user(username):
    if username not in users:
        users.append(username)
        return True
    else:
        return False

def remove_user(username):
    if username in users:
        users.remove(username)

def get_users():
    return users
