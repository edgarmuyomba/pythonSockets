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
            await send(websocket, payload)
        elif payload['operation'] == 'join':
            pass 
        elif payload['operation'] == 'leave':
            pass

async def connect(websocket, data):
    if 'username' in data:
        username = data['username']
        clients[username] = websocket
        current_users = {}
        with open('db/users.json', 'r') as users:
            current_users = json.load(users)
            if username not in current_users:
                current_users.append(username)
        with open('db/users.json', 'w') as users:
            users.write(json.dumps(current_users))
        payload = {
            "code": 200,
            "username": username 
        }
        await websocket.send(json.dumps(payload))

        try:
            await websocket.wait_closed()
        finally:
            del clients[username]
    else:
        await error(websocket, "Please provide a username to register!")

async def send(websocket, data):
    if 'recipient' in data:
        recipient = clients[data['recipient']]
        payload = {
            "code": 201,
            "sender": data['sender'],
            "message": data['message']
        }
        await recipient.send(json.dumps(payload))
    else:
        await error(websocket, "Please provide a recipient for the message!")

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