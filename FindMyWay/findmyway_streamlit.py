import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from PIL import Image, ImageDraw
import math
from simpleai.search import SearchProblem, astar
import streamlit as st
import streamlit.components.v1 as components
from streamlit_drawable_canvas import st_canvas

# Define the maze map
maze_map = """
##############################
#         #              #   #
# ####    ########       #   #
#    #    #              #   #
#    ###     #####  ######   #
#      #   ###   #           #
#      #     #   #  #  #   ###
#     #####    #    #  #     #
#              #       #     #
##############################
"""

maze_map = [list(x) for x in maze_map.split("\n") if x]

cell_size = 21
cost_regular = 1.0
cost_diagonal = 1.7

COSTS = {
    "up": cost_regular,
    "down": cost_regular,
    "left": cost_regular,
    "right": cost_regular
}

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
            if self.board[newy][newx] != "#":
                actions.append(action)
        return actions

    def result(self, state, action):
        x, y = state
        if action.count("up"):
            y -= 1
        if action.count("down"):
            y += 1
        if action.count("left"):
            x -= 1
        if action.count("right"):
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

st.title('Tìm đường trong mê cung')

if "click_count" not in st.session_state:
    st.session_state["click_count"] = 0

if "points" not in st.session_state:
    st.session_state["points"] = []

if "bg_image" not in st.session_state:
    bg_image = Image.open("assets/mecung.bmp")
    st.session_state["bg_image"] = bg_image

canvas_result = st_canvas(
    stroke_width=1,
    stroke_color='',
    background_image=st.session_state["bg_image"],
    height=210,
    width=630,
    drawing_mode="point",
    point_display_radius=0,
    display_toolbar=False,
)

if st.session_state["click_count"] == 2:
    _, col2, _, col4, _, _ = st.columns(6)

    if col2.button('Đường dẫn'):
        if "path_finding_done" not in st.session_state:
            st.session_state["path_finding_done"] = True
            x1, y1 = st.session_state["points"][0]
            x2, y2 = st.session_state["points"][1]

            maze_map[y1][x1] = 'o'
            maze_map[y2][x2] = 'x'
            problem = MazeSolver(maze_map)
            result = astar(problem, graph_search=True)
            path = [x[1] for x in result.path()]
            st.session_state["path"] = path
            draw_frame = st.session_state["bg_image"].copy()
            for p in path:
                x, y = p
                cell_x = x * cell_size + 2
                cell_y = y * cell_size + 2
                frame_temp = ImageDraw.Draw(draw_frame)
                frame_temp.ellipse([cell_x, cell_y, cell_x + cell_size - 4, cell_y + cell_size - 4],
                                   fill="#AEC6CF", outline="#AEC6CF")
            st.session_state["bg_image"] = draw_frame
            st.rerun()

    if col4.button('Chuyển động'):
        if "path_finding_done" in st.session_state:
            path = st.session_state["path"]
            n = len(path)
            px = []
            py = []
            for p in path:
                px.append(p[0] * cell_size + cell_size // 2 - 2)
                py.append(p[1] * cell_size + cell_size // 2 - 2)

            im = plt.imread("assets/mecung.bmp")
            fig, ax = plt.subplots()

            image = ax.imshow(im)
            dest, = ax.plot(px[-1:], py[-1:], "ro", markersize=10)
            red_square, = ax.plot([], [], "ro", markersize=10)

            def init():
                return image, dest, red_square

            def animate(i):
                red_square.set_data(px[:i + 1], py[:i + 1])
                return image, dest, red_square

            anim = FuncAnimation(fig, animate, frames=n, interval=500, init_func=init, repeat=False, blit=True)
            components.html(anim.to_jshtml(), height=550)

    _, col2, _ = st.columns(3)
    col2.text('Nhấn Ctrl-R để chạy lại')

if canvas_result.json_data is not None:
    lst_points = canvas_result.json_data["objects"]
    if len(lst_points) > 0:
        px = lst_points[-1]['left']
        py = lst_points[-1]['top']
        x = int(px) // cell_size
        y = int(py) // cell_size
        if maze_map[y][x] != '#':
            if st.session_state["click_count"] < 2:
                st.session_state["click_count"] += 1
                if st.session_state["click_count"] == 1:
                    cell_x = x * cell_size + 2
                    cell_y = y * cell_size + 2
                    draw_frame = st.session_state["bg_image"].copy()
                    frame_temp = ImageDraw.Draw(draw_frame)
                    frame_temp.ellipse([cell_x, cell_y, cell_x + cell_size - 4, cell_y + cell_size - 4],
                                       fill="#000000", outline="#000000")
                    st.session_state["bg_image"] = draw_frame
                    st.session_state["points"].append((x, y))
                    st.rerun()
                elif st.session_state["click_count"] == 2:
                    cell_x = x * cell_size + 2
                    cell_y = y * cell_size + 2
                    draw_frame = st.session_state["bg_image"].copy()
                    frame_temp = ImageDraw.Draw(draw_frame)
                    frame_temp.ellipse([cell_x, cell_y, cell_x + cell_size - 4, cell_y + cell_size - 4],
                                       fill="#FFB347", outline="#FFB347")
                    st.session_state["bg_image"] = draw_frame
                    st.session_state["points"].append((x, y))
                    st.rerun()
