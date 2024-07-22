import asyncio
import websockets 
import json

from connect4 import PLAYER1, PLAYER2, Connect4

async def handler(websocket):
    game = Connect4()
    isPlayer1 = True
    player = None
    async for message in websocket:
        event = json.loads(message)
        if event['type'] == 'play':
            row = None
            try:
                if isPlayer1:
                    row = game.play(PLAYER1, event['column'])
                    player = PLAYER1
                else:
                    row = game.play(PLAYER2, event['column'])
                    player = PLAYER2
            except RuntimeError as e:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": str(e)
                }))
            else:
                isPlayer1 = not isPlayer1
                await websocket.send(json.dumps({
                    "type": "play",
                    "player": player,
                    "column": event['column'],
                    "row": row
                }))

                if game.last_player_won:
                    await websocket.send(json.dumps({
                        "type": "win",
                        "player": player
                    }))



# async def handler(websocket):
    # while True:
    #     try:
    #         message = await websocket.recv()
    #     except websockets.ConnectionClosedOK:
    #         break
    #     print(message)
    # async for message in websocket:
    #     print(message)


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()

if __name__=="__main__":
    asyncio.run(main())