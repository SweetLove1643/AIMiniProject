import math
from simpleai.search import SearchProblem, astar
import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import time
import os

cost_regular = 1.0
cost_diagonal = 1.4

COSTS = {
    "up": cost_regular,
    "down": cost_regular,
    "left": cost_regular,
    "right": cost_regular,
}

image = cv2.imread(os.path.join(os.getcwd(), "assets\mecung.png"))

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

MAP = []
for row in thresh:
    MAP.append([' ' if pixel == 255 else '#' for pixel in row])

for row in MAP:
    print(''.join(row))

MAX_WIDTH = 50
MAX_HEIGHT = 75

color_converted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
pil_image = Image.fromarray(color_converted)


img_width, img_height = pil_image.size
aspect_ratio = img_width / img_height

if img_width > MAX_WIDTH or img_height > MAX_HEIGHT:
    if aspect_ratio > 1: 
        new_width = MAX_WIDTH
        new_height = int(MAX_WIDTH / aspect_ratio)
    else: 
        new_height = MAX_HEIGHT
        new_width = int(MAX_HEIGHT * aspect_ratio)
else:
    new_width, new_height = img_width, img_height 

pil_image_resized = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)


M = len(MAP)     
N = len(MAP[0])  
W = 3
mau_den  = np.zeros((W, W, 3), np.uint8) + (np.uint8(0), np.uint8(0), np.uint8(0))
mau_trang = np.zeros((W, W, 3), np.uint8) + (np.uint8(255), np.uint8(255), np.uint8(255))
mau_bat_dau = np.zeros((W, W, 3), np.uint8) + (np.uint8(255), np.uint8(0), np.uint8(0))  # Màu đỏ cho điểm bắt đầu
mau_ket_thuc = np.zeros((W, W, 3), np.uint8) + (np.uint8(0), np.uint8(255), np.uint8(0))  # Màu xanh lá cho điểm kết thúc
mau_duong_di = np.zeros((W, W, 3), np.uint8) + (np.uint8(0), np.uint8(0), np.uint8(255))  # Màu xanh dương cho đường đi

image = np.ones((M * W, N * W, 3), np.uint8) * 255 


for x in range(0, M):
    for y in range(0, N):
        if MAP[x][y] == '#':
            image[x * W:(x + 1) * W, y * W:(y + 1) * W] = mau_den
        elif MAP[x][y] == ' ':
            image[x * W:(x + 1) * W, y * W:(y + 1) * W] = mau_trang

color_converted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
pil_image = Image.fromarray(color_converted)



class MazeSolver(SearchProblem):

    def __init__(self, board):
        self.board = board
        self.goal = (0, 0)

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x].lower() == "o":
                    self.initial = (x, y)
                elif self.board[y][x].lower() == "x":
                    self.goal = (x, y)

        super(MazeSolver, self).__init__(initial_state=self.initial)

    def actions(self, state):
        actions = []
        for action in COSTS.keys():
            newx, newy = self.result(state, action)
            if 0 <= newx < len(self.board[0]) and 0 <= newy < len(self.board) and self.board[newy][newx] != "#":
                actions.append(action)

        return actions

    def result(self, state, action):
        x, y = state

        if action == "up":
            y -= 1
        elif action == "down":
            y += 1
        elif action == "left":
            x -= 1
        elif action == "right":
            x += 1

        return (x, y)

    def is_goal(self, state):
        return state == self.goal

    def cost(self, state, action, state2):
        return COSTS[action]

    def heuristic(self, state):
        x, y = state
        gx, gy = self.goal
        return math.sqrt((x - gx) ** 2 + (y - gy) ** 2)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.dem = 0
        self.title('Tìm đường trong mê cung')
        self.cvs_me_cung = tk.Canvas(self, width=N * W, height=M * W,
                                      relief=tk.SUNKEN, border=1)
        
        image_tk = ImageTk.PhotoImage(pil_image_resized)

        self.image_tk = ImageTk.PhotoImage(pil_image)
        self.cvs_me_cung.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

        self.cvs_me_cung.bind("<Button-1>", self.xu_ly_mouse)

        lbl_frm_menu = tk.LabelFrame(self)
        btn_start = tk.Button(lbl_frm_menu, text='Start', width=7,
                              command=self.btn_start_click)
        btn_reset = tk.Button(lbl_frm_menu, text='Reset', width=7,
                              command=self.btn_reset_click)
        btn_start.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N)
        btn_reset.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N)

        self.cvs_me_cung.grid(row=0, column=0, padx=5, pady=5)
        lbl_frm_menu.grid(row=0, column=1, padx=5, pady=7, sticky=tk.NW)

    def xu_ly_mouse(self, event):
        px = event.x
        py = event.y
        x = px // W
        y = py // W

 
        if MAP[y][x] != '#' and self.is_valid_start_end(x, y):
            if self.dem == 0:
                MAP[y][x] = 'o'
                radius = W 
                self.cvs_me_cung.create_oval(
                x * W + (W // 2) - radius, y * W + (W // 2) - radius, 
                (x + 1) * W - (W // 2) + radius, (y + 1) * W - (W // 2) + radius, 
                outline='#FF0000', fill='#FF0000')

                self.dem += 1
            elif self.dem == 1:
                MAP[y][x] = 'x'
                radius = W 
                self.cvs_me_cung.create_rectangle(
                x * W + (W // 2) - radius, y * W + (W // 2) - radius,
                (x + 1) * W - (W // 2) + radius, (y + 1) * W - (W // 2) + radius,
                outline='#FF0000', fill='#FF0000')
                
                self.dem += 1

    def is_valid_start_end(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < N and 0 <= ny < M and MAP[ny][nx] == '#':
                    return False
        return True

    def btn_start_click(self):
        problem = MazeSolver(MAP)

        result = astar(problem, graph_search=True)

        path = [x[1] for x in result.path()]

        L = len(path)

        offset = W 
        step_interval = 3

        for i in range(1, L):
            if i % step_interval == 0:
                x = path[i][0]
                y = path[i][1]
                radius = W * 1.6 
                self.cvs_me_cung.create_oval(
                (x * W + offset) - radius, (y * W + offset) - radius, 
                (x + 1) * W - offset + radius, (y + 1) * W - offset + radius, 
                outline='#0000FF', fill='#ADD8E6')


                time.sleep(0.1)
                self.cvs_me_cung.update()

    def btn_reset_click(self):
        self.cvs_me_cung.delete(tk.ALL)
        self.cvs_me_cung.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        self.dem = 0
        for x in range(0, M):
            for y in range(0, N):
                if MAP[x][y] == 'o' or MAP[x][y] == 'x':
                    MAP[x][y] = ' '


if __name__ == "__main__":
    app = App()
    app.mainloop()
