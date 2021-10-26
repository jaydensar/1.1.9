import turtle

mouse_down = False
count = 0
root = turtle.getcanvas().winfo_toplevel()

# initial state
turtle.color('blue')
turtle.shape('circle')
turtle.penup()
turtle.tracer(0)

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
    turtle.penup()
    goto(x, -y)
    turtle.pendown()

def mouse_up_action(_mouse):
    global mouse_down
    mouse_down=False

def motion_action(mouse):
    if mouse_down:
        x=mouse.x-turtle.window_width()/2
        y=mouse.y-turtle.window_height()/2
        goto(x, -y)

def scroll_action(mouse):
    if mouse.delta<0:
        turtle.pensize(turtle.pensize()-0.5)
    else:
        turtle.pensize(turtle.pensize()+0.5)

def undo_action(_mouse):
    print(int(round(count * 0.05, -1)))
    for _ in range(int(round(count * 0.05, -1)) + 1):
        turtle.undo()
    turtle.update()

root.bind('<ButtonPress-1>', mouse_down_action)
root.bind('<ButtonRelease-1>', mouse_up_action)
root.bind('<Motion>', motion_action)
root.bind('<MouseWheel>', scroll_action)
root.bind('<Control-z>', undo_action)

turtle.mainloop()
