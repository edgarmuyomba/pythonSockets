import asyncio
import websockets 
import json
import secrets

from connect4 import PLAYER1, PLAYER2, Connect4

JOIN = {}

WATCH = {}

async def start(websocket):
    game = Connect4()
    connected = {websocket}

    join_key = secrets.token_urlsafe(12)
    JOIN[join_key] = game, connected

    watch_key = secrets.token_urlsafe(12)
    WATCH[watch_key] = game, connected

    try: 
        event = {
            "type": "init",
            "join": join_key,
            "watch": watch_key
        }
        await websocket.send(json.dumps(event))

        await play(websocket, game, PLAYER1, connected)
    
    finally:
        del JOIN[join_key]
        del WATCH[watch_key]

async def error(websocket, message):
    event = {
        "type": "error",
        "message": message
    }
    await websocket.send(json.dumps(event))

async def join(websocket, join_key):
    try:
        game, connected = JOIN[join_key]
    except KeyError:
        await error(websocket, "Game not found!")
        return 
    
    connected.add(websocket)
    try:
        await play(websocket, game, PLAYER2, connected)
    finally:
        connected.remove(websocket)

async def watch(websocket, watch_key):
    try:
        game, connected = WATCH[watch_key] 
    except KeyError:
        await error(websocket, "Game not found")
        return 

    connected.add(websocket)
    try: 
        await websocket.wait_closed()
    finally:
        connected.remove(websocket)
    

async def handler(websocket):
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"

    if "join" in event:
        await join(websocket, event["join"])
    elif "watch" in event:
        await watch(websocket, event["watch"])
    else:
        await start(websocket)

async def play(websocket, game, player, connected):
    async for message in websocket:
        event = json.loads(message)
        if event['type'] == 'play':
            row = None
            try:
                row = game.play(player, event['column'])
            except RuntimeError as e:
                for connection in connected:
                    await error(connection, str(e))
            else:
                websockets.broadcast(connected, json.dumps({
                        "type": "play",
                        "player": player,
                        "column": event['column'],
                        "row": row
                    }))

                if game.winner != None:
                    websockets.broadcast(connected, json.dumps({
                            "type": "win",
                            "player": game.winner
                        }))

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()

if __name__=="__main__":
    asyncio.run(main())