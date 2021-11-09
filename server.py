import asyncio
import json

import websockets
from jsonschema import ValidationError, validate

clients = set()

msgs = []

schemas = {
    "update": {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
            "x": {"type": "number", "minimum": -100000, "maximum": 100000},
            "y": {"type": "number", "minimum": -100000, "maximum": 100000},
            "pen_down": {"type": "boolean"},
            "pen_size": {"type": "integer", "minimum": 0, "maximum": 100},
            "color": {
                "type": "array",
                "items": {
                    "type": ["array", "string"],
                    "pattern": "white|black|red|green|blue|cyan|yellow|magenta",
                    "items": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1
                    }
                }
            },
            "socket_id": {"type": "string", "format": "uuid"},
        },
        "additionalProperties": False,
        "minProperties": 7
    },
    "undo": {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
            "socket_id": {"type": "string", "format": "uuid"},
            "count": {"type": "integer", "minimum": 0, "maximum": 1000}
        },
        "additionalProperties": False,
        "minProperties": 3
    },
    "clear": {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
            "socket_id": {"type": "string", "format": "uuid"}
        },
        "additionalProperties": False,
        "minProperties": 2
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
            except ValidationError as err:
                print("Invalid json data passed; schema incorrect: ", err)
                continue
            except json.JSONDecodeError as err:
                print("Invalid json data passed; not json: ", err)
            except:
                print("Something went wrong, ignoring data from ", websocket)

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
