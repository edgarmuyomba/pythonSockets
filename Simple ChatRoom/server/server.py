import websockets
import asyncio
import json
from uuid import uuid4
import utils
from datetime import datetime

clients = {}

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()


async def handler(websocket):
    async for message in websocket:
        payload = json.loads(message)
        if payload['operation'] == 'connect':
            await connect(websocket, payload)
        elif payload['operation'] == 'send':
            await send(websocket, payload)
        elif payload['operation'] == 'receive':
            await receive(websocket, payload)


async def connect(websocket, data):
    if 'username' in data and data['username'] != "":
        username = data['username']
        created = utils.add_user(username)
        if created:
            clients[username] = websocket
            payload = {
                "code": 200,
                "username": username
            }
            await websocket.send(json.dumps(payload))

            users = utils.get_users()
            users_payload = {
                "code": 202,
                "data": users
            }
            await sendBroadcast(json.dumps(users_payload))
        else:
            await error(websocket, "This username is already taken!")
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


async def receive(websocket, data):
    message = data['message']
    sender = data['sender']
    payload = {
        "code": 205,
        "sender": sender,
        "message": message,
        "time": datetime.now().strftime("%H:%M")
    }

    await sendBroadcast(json.dumps(payload))

async def sendBroadcast(jsonPayload, exclude=None):
    users = utils.get_users()
    connected = [clients[user] for user in users if user != exclude]
    websockets.broadcast(connected, jsonPayload)

async def error(websocket, message):
    payload = {
        "code": 400,
        "message": message
    }
    await websocket.send(json.dumps(payload))

if __name__ == '__main__':
    asyncio.run(main())
