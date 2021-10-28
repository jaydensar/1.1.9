import json
import uuid
import turtle
import asyncio
import websockets

from queue import Queue
from threading import Thread
from asyncio.tasks import Task
from tkinter import colorchooser

mouse_down = False
count = 0
stroke_history = [0]
root = turtle.getcanvas().winfo_toplevel()

# initial state
root.config(cursor="none")
turtle.color('blue')
turtle.shape('circle')
turtle.penup()
turtle.tracer(0)
turtle.pensize(1)
turtle.shapesize(turtle.pensize()*0.05)
turtle.update()

def round_min(value, min):
    if value>=0.5:
        return value
    else:
        return min

def goto(x,y):
    global count
    print("moving to", x, y)
    turtle.goto(x,y)
    turtle.update()
    count+=1
    print(count)

def mouse_down_action(mouse):
    global mouse_down
    mouse_down=True
    x=mouse.x-turtle.window_width()/2
    y=mouse.y-turtle.window_height()/2
    stroke_history.insert(0, 0)
    turtle.penup()
    goto(x, -y)
    turtle.pendown()

def mouse_up_action(_mouse):
    global mouse_down
    mouse_down=False

def motion_action(mouse):
    if mouse_down:
        turtle.pendown()
    else:
        turtle.penup()
    stroke_history[0] = stroke_history[0] + 1
    print(stroke_history)
    x=mouse.x-turtle.window_width()/2
    y=mouse.y-turtle.window_height()/2
    socket_queue.put({
        'x': x,
        'y': -y,
        'pen_down': mouse_down,
        'pen_size': turtle.pensize(),
        'shape_size': turtle.shapesize(),
        'color': turtle.color(),
        'socket_id': socket_id
    })
    goto(x, -y)

def scroll_action(mouse):
    if mouse.delta<0:
        turtle.pensize(round_min(turtle.pensize()-2, 2))
    else:
        turtle.pensize(turtle.pensize()+2)
    turtle.shapesize(turtle.pensize()*0.05)
    turtle.update()
    print(turtle.pensize(),turtle.shapesize())

def undo_action(_mouse):
    for _ in range(stroke_history[0]):
        turtle.undo()
    stroke_history.pop(0)
    turtle.update()

def color_choose(_key):
    color=colorchooser.askcolor()[1]
    turtle.pencolor(color)
    turtle.color(color)

root.bind('<ButtonPress-1>', mouse_down_action)
root.bind('<ButtonRelease-1>', mouse_up_action)
root.bind('<Motion>', motion_action)
root.bind('<MouseWheel>', scroll_action)
root.bind('<Control-z>', undo_action)
root.bind('<c>', color_choose)

# socket 
socket_queue = Queue()
socket_id = str(uuid.uuid4())
socket_draw_queue = Queue()

async def send(websocket):
    while True:
        obj = socket_draw_queue.get()
        await websocket.send(json.dumps(obj))
async def receive(websocket):
    while True:
        a = await websocket.recv()
        data = json.loads(a)
        if data['socket_id'] == socket_id:
            return
        socket_draw_queue.put(data)
        print(f"received {data}")

async def socket():
    async with websockets.connect("ws://localhost:8765") as websocket:
        send_thread = Thread(target=asyncio.run, daemon=True, args=(send(websocket),))
        receive_thread = Thread(target=asyncio.run, daemon=True, args=(receive(websocket),))
        send_thread.start()
        receive_thread.start()

asyncio.run(socket())

turtle.mainloop()
