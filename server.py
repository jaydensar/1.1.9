import asyncio
import json

import websockets
from jsonschema import validate

clients = set()

msgs = []

schemas = {
    "update": {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
            "x": {"type": "number"},
            "y": {"type": "number"},
            "pen_down": {"type": "boolean"},
            "pen_size": {"type": "number"},
            "color": {"type": "array"},
            "socket_id": {"type": "string"}
        }
    },
    "undo": {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
            "socket_id": {"type": "string"},
            "count": {"type": "number"}
        }
    },
    "clear": {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
            "socket_id": {"type": "string"}
        }
    }
}


async def handler(websocket, path):
    global msgs
    clients.add(websocket)
    await websocket.send(json.dumps({'type': 'init', 'data': msgs}))
    try:
        async for msg in websocket:
            try:
                data = json.loads(msg)
                validate(data, schemas[data['type']])
                if (data['type'] == 'reset'):
                    msgs = []
            except:
                continue
            msgs.append(msg)
            await asyncio.gather(
                *[ws.send(msg) for ws in clients],
                return_exceptions=False,
            )
    finally:
        clients.remove(websocket)


async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()

asyncio.run(main())
