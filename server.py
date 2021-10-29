import websockets
import asyncio
import json

clients = set()

msgs = []


async def handler(websocket, path):
    global msgs
    clients.add(websocket)
    await websocket.send(json.dumps({'type': 'init', 'data': msgs}))
    try:
        async for msg in websocket:
            msgs.append(msg)
            if ("reset" in msg):
                msgs = []
            await asyncio.gather(
                *[ws.send(msg) for ws in clients],
                return_exceptions=False,
            )
    finally:
        clients.remove(websocket)


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())
