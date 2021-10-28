import json
import uuid
import turtle
import websocket

from threading import Thread
from queue import Queue, Empty
from tkinter import colorchooser

# configurable options
PRECISION = 5  # lower is smoother, but slower
OFFLINE = False  # skip connecting to websocket server
LOAD_PREVIOUS = True  # whether or not to load people's previous drawings
SOCKET_INSTANCE = "ws://119.jaydensar.net:8765" # set to socket instance (server.py)


# internal variables
count = 0
stroke_history = [0]
precision = int(PRECISION)
root = turtle.getcanvas().winfo_toplevel()

remote_turtles: dict[str, turtle.Turtle] = {}

# initial state
root.config(cursor="none")
turtle.color('blue')
turtle.shape('circle')
turtle.penup()
turtle.tracer(0)
turtle.pensize(2)
turtle.shapesize(turtle.pensize()*0.05)
turtle.update()


def round_min(value, min):
    if value >= min:
        return value
    else:
        return min


def goto(x, y):
    global count
    global precision
    if precision == PRECISION:
        precision = 0
        print("moving to", x, y)
        turtle.goto(x, y)
        turtle.update()
        socket_queue.put({
            'type': 'update',
            'x': x,
            'y': y,
            'pen_down': turtle.pen()['pendown'],
            'pen_size': turtle.pensize(),
            'color': turtle.color(),
            'socket_id': socket_id
        })
        count += 1
        print(count)
    else:
        precision += 1
        print("skipping")


def mouse_down_action(mouse):
    x = mouse.x-turtle.window_width()/2
    y = -(mouse.y-turtle.window_height()/2)
    stroke_history.insert(0, 0)
    stroke_history[0] = stroke_history[0] + 1
    goto(x, y)
    turtle.pendown()


def mouse_up_action(_mouse):
    turtle.penup()


def motion_action(mouse):
    stroke_history[0] = stroke_history[0] + 1
    print('stroke:'+str(stroke_history))
    x = mouse.x-turtle.window_width()/2
    y = -(mouse.y-turtle.window_height()/2)
    goto(x, y)


def scroll_action(mouse):
    if mouse.delta < 0:
        turtle.pensize(round_min(turtle.pensize()-2, 2))
    else:
        turtle.pensize(turtle.pensize()+2)
    turtle.shapesize(turtle.pensize()*0.05)
    turtle.update()
    print(turtle.pensize(), turtle.shapesize())


def undo_action(_mouse):
    global stroke_history
    undo_count = 0
    for _ in range(stroke_history[0]):
        turtle.undo()
        undo_count += 1
    stroke_history.pop(0)
    if len(stroke_history) == 0:
        stroke_history = [0]

    socket_queue.put({
        'type': 'undo',
        'socket_id': socket_id,
        'count': undo_count
    })
    turtle.update()


def color_choose(_key):
    color = colorchooser.askcolor()[1]
    turtle.pencolor(color)
    turtle.color(color)


root.bind('<ButtonPress-1>', mouse_down_action)
root.bind('<ButtonRelease-1>', mouse_up_action)
root.bind('<Motion>', motion_action)
root.bind('<MouseWheel>', scroll_action)
root.bind('<Control-z>', undo_action)
root.bind('<c>', color_choose)

socket_queue = Queue()
socket_id = str(uuid.uuid4())
socket_draw_queue = Queue()


def draw():
    global remote_turtles
    print("running")
    data = None
    try:
        data = socket_draw_queue.get(block=False)
    except Empty:
        pass
    # print(data)
    if (data is None):
        root.after(100, draw)
        return

    print(data['type'])

    if data['type'] == 'update':
        print("type is update")
        if not data['socket_id'] in remote_turtles:
            remote_turtles[data['socket_id']] = turtle.Turtle()
            remote_turtle = remote_turtles[data['socket_id']]
            remote_turtle.penup()
            remote_turtle.color(data['color'][0])
            remote_turtle.shape('circle')
            remote_turtle.pensize(data['pen_size'])
            remote_turtle.shapesize(data['pen_size']*0.05)

        remote_turtle = remote_turtles[data['socket_id']]
        remote_turtle.goto(data['x'], data['y'])
        remote_turtle.pendown() if data['pen_down'] else remote_turtle.penup()
        remote_turtle.pensize(data['pen_size'])
        remote_turtle.shapesize(data['pen_size']*0.05)
        remote_turtle.color(data['color'][0])
        turtle.update()
        root.after(0, draw)
        return

    if data['type'] == 'init':
        if LOAD_PREVIOUS:
            for turtle_data_json in data['data']:
                turtle_data = json.loads(turtle_data_json)
                print("doing action", turtle_data)
                if turtle_data['type'] == 'undo':
                    try:
                        remote_turtle = remote_turtles[data['socket_id']]

                        for _ in range(data['count']):
                            remote_turtle.undo()
                    except:
                        pass
                    continue
                if not turtle_data['socket_id'] in remote_turtles:
                    remote_turtles[turtle_data['socket_id']] = turtle.Turtle()
                    remote_turtle = remote_turtles[turtle_data['socket_id']]
                    remote_turtle.penup()
                    remote_turtle.color(turtle_data['color'][0])
                    remote_turtle.shape('circle')
                    remote_turtle.pensize(turtle_data['pen_size'])
                    remote_turtle.shapesize(turtle_data['pen_size']*0.05)
                remote_turtle = remote_turtles[turtle_data['socket_id']]
                remote_turtle.goto(turtle_data['x'], turtle_data['y'])
                remote_turtle.pendown(
                ) if turtle_data['pen_down'] else remote_turtle.penup()
                remote_turtle.pensize(turtle_data['pen_size'])
                remote_turtle.shapesize(turtle_data['pen_size']*0.05)
                remote_turtle.color(turtle_data['color'][0])
            turtle.update()
            remote_turtles = {}
            root.after(100, draw)

    if data['type'] == 'undo':
        remote_turtle = remote_turtles[data['socket_id']]

        for _ in range(data['count']):
            remote_turtle.undo()

        turtle.update()
        root.after(0, draw)


def socket():
    def on_message(ws, message):
        data = json.loads(message)
        if data['type'] == 'update' and data['socket_id'] == socket_id:
            return
        socket_draw_queue.put(data)
        print(message)

    def on_error(ws, error):
        print(error)

    def on_close(ws, close_status_code, close_msg):
        print(f"socket closed: {close_status_code} {close_msg}")

    def on_open(ws):
        def run(*args):
            while True:
                s = socket_queue.get()
                ws.send(json.dumps(s))
        Thread(target=run, args=()).start()

    ws = websocket.WebSocketApp(SOCKET_INSTANCE,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()


if not OFFLINE:
    root.after(1, draw)
    Thread(target=socket, daemon=True).start()

turtle.mainloop()
