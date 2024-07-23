import asyncio
import websockets
import json

async def connect():
    uri = "ws://127.0.0.1:8001"
    async with websockets.connect(uri) as client:
        payload = {
            'operation': 'connect',
            'username': 'edgarmatthew'
        }

        await client.send(json.dumps(payload))

        while True:

            response = await client.recv()
            data = json.loads(response)

            # if data['code'] == 200:
            #     print("Logged in!")

            #     while True:
            #         recipient = input("Recipient: ")
            #         message = input("Message: ")
            #         payload = {
            #             'operation': 'send',
            #             'recipient': recipient,
            #             'sender': 'edgarmatthew',
            #             'message': message 
            #         }
            #         await client.send(json.dumps(payload))
            # elif data['code'] == 400:
            #     print(data['message'])
            # elif data['code'] == 201:
            #     print(f"{data['sender']} says {data['message']}")
            print(data)

if __name__=="__main__":
    asyncio.run(connect())