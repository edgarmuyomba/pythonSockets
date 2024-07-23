import asyncio
import websockets
import json

async def connect():
    uri = "ws://127.0.0.1:8001"
    async with websockets.connect(uri) as client:
        payload = {
            'operation': 'connect',
            'username': 'Edgar again'
        }

        await client.send(json.dumps(payload))

        response = await client.recv()
        data = json.loads(response)
        print(data)
        await client.close()

if __name__=="__main__":
    asyncio.run(connect())