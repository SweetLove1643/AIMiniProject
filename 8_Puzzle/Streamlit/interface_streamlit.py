import streamlit as st
from PIL import Image
import main

algorithm = None
initialState = None
statepointer = cost = counter = depth = 0
runtime = 0.0
path = []

st.title("Giải pháp 8-Puzzle")
st.markdown("### Chọn thuật toán tìm kiếm và trạng thái ban đầu")

algorithm = st.selectbox(
    'Chọn thuật toán tìm kiếm:',
    ['BFS', 'UCS', 'HillClimbing', 'IDFS', 'DFS', 'Greedy', 'A*']
)

initialState = st.text_input('Nhập trạng thái ban đầu (9 chữ số, ví dụ: "123456780")')

def print_path_as_matrix(path):
    for state in path:
        state = str(state).zfill(9)  
        if len(state) == 9:
            st.write("Trạng thái:")
            for i in range(0, 9, 3): 
                row = state[i:i+3] 
                st.write(" ".join(row)) 
            st.write("\n") 
        else:
            st.warning(f"Trạng thái không hợp lệ: {state}")


if st.button("Giải quyết"):
    if initialState and algorithm:
        st.text(f"Đang giải bài toán bằng thuật toán {algorithm} với trạng thái ban đầu {initialState}")
        
        
        if algorithm == 'BFS':
            main.BFS(initialState)
            path, cost, counter, depth, runtime = main.bfs_path, main.bfs_cost, main.bfs_counter, main.bfs_depth, main.time_bfs
        elif algorithm == 'UCS':
            main.UCS(initialState)
            path, cost, counter, depth, runtime = main.ucs_path, main.ucs_cost, main.ucs_counter, main.ucs_depth, main.time_ucs
        elif algorithm == 'HillClimbing':
            main.hillClimbingWithRandomRestart(initialState, max_restarts=1000)
            path, cost, counter, depth, runtime = main.hc_path, main.hc_cost, main.hc_counter, main.hc_depth, main.time_hc
        elif algorithm == 'IDFS':
            main.IDFS(initialState, 10)
            path, cost, counter, depth, runtime = main.idfs_path, main.idfs_cost, main.idfs_counter, main.idfs_depth, main.time_idfs
        elif algorithm == 'DFS':
            main.DFS(initialState)
            path, cost, counter, depth, runtime = main.dfs_path, main.dfs_cost, main.dfs_counter, main.dfs_depth, main.time_dfs
        elif algorithm == 'Greedy':
            main.GreedyManhattan(initialState)
            path, cost, counter, depth, runtime = main.manhattan_path, main.manhattan_cost, main.manhattan_counter, main.manhattan_depth, main.time_manhattan
        elif algorithm == 'A*':
            main.AStarSearch_euclid(initialState)
            path, cost, counter, depth, runtime = main.euclid_path, main.euclid_cost, main.euclid_counter, round(main.euclid_depth), main.time_euclid
        
        
        st.write(f"Số nút đã mở rộng: {counter}")
        st.write(f"Chiều sâu tìm kiếm: {depth}")
        st.write(f"Chi phí tìm kiếm: {cost}")
        st.write(f"Thời gian chạy: {runtime} s")
        
        
        st.write(f"Đường đi giải pháp: {path}")
        
        
        print_path_as_matrix(path)

    else:
        st.error("Vui lòng chọn thuật toán và cung cấp trạng thái ban đầu hợp lệ!")


if st.button("Làm mới"):
    st.session_state.clear()
