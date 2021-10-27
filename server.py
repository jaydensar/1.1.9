import websockets
import asyncio

CLIENTS = set()

async def handler(websocket, path):
    CLIENTS.add(websocket)
    try:
        async for msg in websocket:
            await asyncio.gather(
                *[ws.send(msg) for ws in CLIENTS],
                return_exceptions=False,
            )
    finally:
        CLIENTS.remove(websocket)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
