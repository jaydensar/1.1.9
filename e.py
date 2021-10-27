 # async def socket():
    #     
    #         async def read_from_socket():
    #             while True:
    #                 obj = queue.get()
    #                 await websocket.send(json.dumps(obj))
    #                 a = await websocket.recv()
    #                 data = json.loads(a)
    #                 if data['socket_id'] == socket_id:
    #                    continue
    #                 socket_draw_queue.put(data)
    #                 print(f"received {data}")