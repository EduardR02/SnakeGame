import random
import tkinter as tk
from pynput import keyboard

grid_size = 30
grid_count = 28
blob_size = grid_size - 2
window_size = grid_size * grid_count
back_color = "#171717"
snake_Color = "#4ca3dd"
apple_color = "#ff4040"
blobs = []
apple_m = None
start_size = 2
apple_boost = 100
dead = True
current_direction = 0
input_direction = 0
y_cor = []
x_cor = []
score = 0
my_font = "Courier 15 bold"
ms_time = 100


def add_blobs(c1):
    if len(blobs) != 0:
        temp = blobs[len(blobs) - 1]
        for i in range(apple_boost):
            create_blob(temp.get_x(), temp.get_y())
            x_cor.append(temp.get_x())
            y_cor.append(temp.get_y())
            blobs[-1].show_blob(c1)


def dead_check():
    global dead
    for i in range(len(blobs) - 1):
        if blobs[0].get_x() == blobs[i + 1].get_x() and blobs[0].get_y() == blobs[i + 1].get_y():
            dead = True


def determine_direction():
    global current_direction, input_direction
    if input_direction == 0 and current_direction != 1:
        current_direction = 0

    if input_direction == 1 and current_direction != 0:
        current_direction = 1

    if input_direction == 2 and current_direction != 3:
        current_direction = 2

    if input_direction == 3 and current_direction != 2:
        current_direction = 3


def key_control(key):
    global input_direction, dead
    try:
        x = key.char
    except AttributeError:
        x = key

    if x == "w" or x == keyboard.Key.up:
        input_direction = 2
    if x == "a" or x == keyboard.Key.left:
        input_direction = 0
    if x == "s" or x == keyboard.Key.down:
        input_direction = 3
    if x == "d" or x == keyboard.Key.right:
        input_direction = 1
    if x == keyboard.Key.esc:
        dead = True


def update_head_pos():
    global current_direction
    if current_direction == 0:
        blobs[0].x_minus_one()
    if current_direction == 1:
        blobs[0].x_plus_one()
    if current_direction == 2:
        blobs[0].y_minus_one()
    if current_direction == 3:
        blobs[0].y_plus_one()


def update(c1):
    global dead, score
    if not dead:
        y_cor.clear()
        x_cor.clear()
        determine_direction()

        for i in blobs:
            y_cor.append(i.get_y())
            x_cor.append(i.get_x())

        for i in range(len(blobs) - 1):
            blobs[i + 1].set_x(x_cor[i])
            blobs[i + 1].set_y(y_cor[i])

        update_head_pos()
        dead_check()

        if apple_m.get_x() == blobs[0].get_x() and apple_m.get_y() == blobs[0].get_y():
            add_blobs(c1)
            create_apple(c1)
            score += apple_boost


def start(c1):
    global dead, current_direction, blobs, score, start_size, input_direction
    if dead:
        blobs.clear()
        x_cor.clear()
        y_cor.clear()
        if start_size == 0:
            start_size = 1
        for i in range(start_size):
            create_blob(grid_count / 2 + i, grid_count / 2)

        create_apple(c1)
        dead = False
        current_direction = 0
        input_direction = 0
        score = 0


def reset_game(master, c1, sc):
    global apple_m, dead
    dead = True
    for i in blobs:
        i.del_obj(c1)
    apple_m.del_obj(c1)
    apple_m = None
    start(c1)
    show_all_blobs(c1)
    logic(master, c1, sc)


def center(master):
    master.update_idletasks()
    x = (master.winfo_screenwidth() // 2) - (window_size // 2)
    y = (master.winfo_screenheight() // 2) - (window_size // 2)
    master.geometry('{}x{}+{}+{}'.format(window_size, window_size, x, y))


def show_all_blobs(c1):
    if len(blobs) != 0:
        for i in blobs:  # not sure if i is int or object : ok i know now, i is object not int
            i.show_blob(c1)


def move_all_blobs(c1):
    if len(blobs) != 0:
        j = 0
        for i in blobs:
            x = x_cor[j]
            y = y_cor[j]
            i.move_blob(i.get_x() - x, i.get_y() - y, c1)
            j += 1


def create_blob(posx, posy):
    blob1 = Blob(posx, posy, False)
    blobs.append(blob1)


def get_random_grid():
    return random.randint(0, grid_count - 1)


def create_apple(c1):
    global apple_m
    if apple_m is not None:
        apple_m.del_obj(c1)

    x = get_random_grid()
    y = get_random_grid()
    on_snake = True
    if len(blobs) != 0:
        while on_snake:
            on_snake = False
            for i in blobs:
                if i.get_x() == x and i.get_y() == y:
                    x = get_random_grid()
                    y = get_random_grid()
                    on_snake = True

    apple_m = Blob(x, y, True)
    apple_m.show_blob(c1)


class Blob:
    def __init__(self, x, y, apple):
        self.x = x
        self.y = y
        self.apple = apple
        self.col = snake_Color
        if apple:
            self.col = apple_color
        self.obj = None

    def del_obj(self, c1):
        c1.delete(self.obj)

    def move_blob(self, x, y, c1):
        c1.move(self.obj, x * grid_size, y * grid_size)

    def show_blob(self, c1):
        self.obj = c1.create_rectangle(self.x * grid_size + 1, self.y * grid_size + 1,
                                       self.x * grid_size + blob_size + 1, self.y * grid_size + blob_size + 1,
                                       outline=self.col, fill=self.col)

    def x_plus_one(self):
        global dead
        self.x = self.x + 1
        if self.x > grid_count - 1:
            dead = True

    def x_minus_one(self):
        global dead
        self.x = self.x - 1
        if self.x < 0:
            dead = True

    def y_plus_one(self):
        global dead
        self.y = self.y + 1
        if self.y > grid_count - 1:
            dead = True

    def y_minus_one(self):
        global dead
        self.y = self.y - 1
        if self.y < 0:
            dead = True

    def get_col(self):
        return self.col

    def set_col(self, col):
        self.col = col

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y

    def get_apple(self):
        return self.apple

    def set_apple(self, apple):
        self.apple = apple


def logic(master, c1, sc):
    c1.itemconfig(sc, text=f"Score: {score}")
    if not dead:
        update(c1)
        move_all_blobs(c1)
        master.after(ms_time, logic, master, c1, sc)
    else:
        reset_game(master, c1, sc)


def the_start():
    root = tk.Tk()
    root.title("Python - haha")
    root.resizable(0, 0)
    center(root)
    canvas = tk.Canvas(root, height=window_size, width=window_size, bg=back_color)
    scoreboard = canvas.create_text(60, 20, text=f"Score: {score}", fill=apple_color, font=my_font)
    canvas.pack()
    li = keyboard.Listener(on_press=key_control)
    li.start()
    start(canvas)
    show_all_blobs(canvas)
    root.after(ms_time, logic, root, canvas, scoreboard)
    root.mainloop()


if __name__ == "__main__":
    the_start()
