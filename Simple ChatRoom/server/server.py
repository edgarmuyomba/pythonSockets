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
        elif payload['operation'] == 'join':
            pass
        elif payload['operation'] == 'leave':
            pass


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

            # await asyncio.sleep(1)

            users = utils.get_users()
            users_payload = {
                "code": 202,
                "data": users
            }
            await sendBroadcast(json.dumps(users_payload))

            # await timer(websocket)
        else:
            await error(websocket, "This username is already taken!")

        try:
            await websocket.wait_closed()
            print(f"{websocket} left the chat.")
        finally:
            del clients[username]
            utils.remove_user(username)
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
        "time": datetime.now().strftime("%H:%M:%S")
    }

    await sendBroadcast(json.dumps(payload))

def join(websocket, data):
    pass


def leave(websocket, data):
    pass

async def sendBroadcast(jsonPayload, exclude=None):
    users = utils.get_users()
    connected = [clients[user] for user in users if user != exclude]
    websockets.broadcast(connected, jsonPayload)

async def timer(websocket):

    while True:

        current_time = datetime.now().strftime("%H:%M:%S")

        payload = {
            "code": 205,
            "sender": "Server",
            "message": f"The time is {current_time}",
            "time": current_time
        }

        await sendBroadcast(json.dumps(payload))

        await asyncio.sleep(5)


async def error(websocket, message):
    payload = {
        "code": 400,
        "message": message
    }
    await websocket.send(json.dumps(payload))

if __name__ == '__main__':
    asyncio.run(main())
