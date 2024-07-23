import websockets
import asyncio 
import json
from uuid import uuid4

clients = {}

async def main():
    async with websockets.serve(handler, "127.0.0.1", 8001):
        await asyncio.Future()

async def handler(websocket):
    async for message in websocket:
        payload = json.loads(message)
        if payload['operation'] == 'connect':
            await connect(websocket, payload)
        elif payload['operation'] == 'send':
            pass 
        elif payload['operation'] == 'join':
            pass 
        elif payload['operation'] == 'leave':
            pass

async def connect(websocket, data):
    if 'username' in data:
        id = str(uuid4())
        username = data['username']
        clients[id] = websocket
        current_users = {}
        with open('db/users.json', 'r') as users:
            current_users = json.load(users)
            current_users[id] = username
        with open('db/users.json', 'w') as users:
            users.write(json.dumps(current_users))
        payload = {
            "code": 200,
            "id": id,
            "username": username 
        }
        await websocket.send(json.dumps(payload))
    else:
        await error(websocket, "Please provide a username to register!")

def send(websocket, data):
    pass 

def join(websocket, data):
    pass 

def leave(websocket, data):
    pass 

async def error(websocket, message):
    payload = {
        "code": 400,
        "message": message
    }
    await websocket.send(json.dumps(payload))

if __name__=='__main__':
    asyncio.run(main())