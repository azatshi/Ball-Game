from tkinter import *
import tkinter.messagebox
import random
import time

class Ball:
    def __init__(self, canvas, paddle, color):
        self.paddle = paddle
        self.canvas = canvas
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
        self.points = 0
        
    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False
        
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = random.randint(3, 3 + self.points // 3)
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos) == True:
            self.y = -(random.randint(3,3 + self.points // 3))
            self.points += 1
                            
        if pos[0] <= 0:
            self.x = random.randint(3,3 + self.points // 3)
        if pos[2] >= self.canvas_width:
            self.x = -(random.randint(3,3 + self.points // 3))

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        
    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 5:
            self.x = 2
        elif pos[2] >= self.canvas_width-5:
            self.x = -2
    def turn_left(self, evt):
        self.x = -5 
    def turn_right(self, evt):
        self.x = 5

tk = Tk()
tk.title("Игра")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)


canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()
paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, paddle, 'red')

label_text = Label(text="Счёт: ", font="Arial 32")
label_points = Label(text="0", font="Arial 32")
label_text.pack(side = LEFT, pady=15)
label_points.pack(side = RIGHT, pady=15)

start_game = tkinter.messagebox.askyesno( 'Прыг-скок', 'Начать игру?')
if not start_game:
    tk.destroy()
while start_game:  
        if ball.hit_bottom == False:
            ball.draw()
            paddle.draw()
            label_points['text'] = ball.points
        else:
            answer = tkinter.messagebox.askyesno( 'Игра', 'Поражение' + '\n' + \
    'Ваш счёт: ' + str(ball.points) + '\n' + 'Начать заново?')
            if answer:
                canvas.delete('all')
                ball.hit_bottom = False
                ball.points = 0
                paddle = Paddle(canvas, 'blue')
                ball = Ball(canvas, paddle, 'red')
            else:
                tk.destroy()
                break
        tk.update_idletasks()
        tk.update()
        time.sleep(0.01)
