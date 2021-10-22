import turtle
turtle.color('blue')
turtle.speed(0)
turtle.shape('circle')

value=False

def mouse_down(mouse):
    global value
    value=True
    x=mouse.x-turtle.window_width()/2
    y=mouse.y-turtle.window_height()/2
    turtle.penup()
    turtle.goto(x, -y)
    turtle.pendown()
def mouse_up(mouse):
    global value
    value=False
def motion(mouse):
    if value:
        x=mouse.x-turtle.window_width()/2
        y=mouse.y-turtle.window_height()/2
        print(x,y)
        turtle.goto(x, -y)
def scroll(mouse):
    if mouse.delta<0:
        turtle.pensize(turtle.pensize()-0.5)
    else:
        turtle.pensize(turtle.pensize()+0.5)

turtle.getcanvas().winfo_toplevel().bind('<ButtonPress-1>', mouse_down)
turtle.getcanvas().winfo_toplevel().bind('<ButtonRelease-1>', mouse_up)
turtle.getcanvas().winfo_toplevel().bind('<Motion>', motion)
turtle.getcanvas().winfo_toplevel().bind('<MouseWheel>', scroll)

turtle.mainloop()
