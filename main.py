import turtle
turtle.color('blue')
turtle.speed(0)
turtle.shape('circle')
turtle.penup()

value=False
move=False
count=0

def goto(x,y):
    global move
    global count
    if move:
        print("moving to", x, y)
        turtle.goto(x,y)
        count+=1
        print(count)
        move=False
    else:
        move=True
        print("not moving")

def mouse_down(mouse):
    global value
    value=True
    x=mouse.x-turtle.window_width()/2
    y=mouse.y-turtle.window_height()/2
    turtle.penup()
    goto(x, -y)
    turtle.pendown()
def mouse_up(mouse):
    global value
    value=False
def motion(mouse):
    if value:
        x=mouse.x-turtle.window_width()/2
        y=mouse.y-turtle.window_height()/2
        # print(x,y)
        goto(x, -y)
def scroll(mouse):
    if mouse.delta<0:
        turtle.pensize(turtle.pensize()-0.5)
    else:
        turtle.pensize(turtle.pensize()+0.5)

def undo(_mouse):
    turtle.undo()

turtle.getcanvas().winfo_toplevel().bind('<ButtonPress-1>', mouse_down)
turtle.getcanvas().winfo_toplevel().bind('<ButtonRelease-1>', mouse_up)
turtle.getcanvas().winfo_toplevel().bind('<Motion>', motion)
turtle.getcanvas().winfo_toplevel().bind('<MouseWheel>', scroll)
turtle.getcanvas().winfo_toplevel().bind('<Control-z>', undo)

turtle.mainloop()
