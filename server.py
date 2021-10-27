import websockets
import asyncio

clients = set()

async def handler(websocket, path):
    clients.add(websocket)
    try:
        async for msg in websocket:
            print(msg)
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
