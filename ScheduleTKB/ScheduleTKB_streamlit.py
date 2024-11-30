import streamlit as st
import streamlit.components.v1 as components
from streamlit_drawable_canvas import st_canvas
from constraint import *
from time import time

P_6352 = ['ARIN330585_01', 'ARIN330585_02']
P_7084 = ['ARIN330585_03CLC', 'INPR140285_07', 'INPR140285_08', 'INPY131685_06', 'INPY131685_07']
P_9079 = ['ARIN330585_04CLC', 'ARIN330585_05CLC', 'ARIN330585_06CLC', 'ARIN330585_07CLC', 'DIPR430685_01', 'DIPR430685_02', 'INPY131685_10', 'INPY131685_11']
P_9831 = ['ARIN330585E_01FIE', 'ARIN330585E_02FIE', 'DIGR230485E_01FIE', 'DIGR230485E_02FIE']
P_0623 = ['ARIN330585E_03FIE', 'MALE431085E_01FIE']
P_3995 = ['BDPR431385_01', 'BDPR431385_02CLC']
P_2151 = ['DIGR230485_02CLC', 'DIGR230485_03CLC', 'DIGR230485_04CLC', 'ITAP138785_07', 'ITAP138785_08']
P_0562 = ['DIGR230485E_03FIE']
P_3984 = ['DIPR430685_01CLC', 'DLEA432085E_01FIE', 'DLEA432085E_02FIE']
P_0309 = ['DLEA432085_01', 'DLEA432085_02CLC', 'INPR130285_01', 'INPR130285E_02FIE', 'INPR140285_01', 'INPR140285_02', 'INPR140285_03', 'INPR140285_04']
P_7094 = ['INIT130185_01', 'INIT130185_02', 'INIT130185_03', 'INIT130185_04']
P_2148 = ['INIT130185E_01FIE', 'INIT130185E_02FIE']
P_9153 = ['INPR130285E_01FIE', 'INPR140285_05', 'INPR140285_06']
P_1352 = ['INPY131685_05']
P_6452 = ['INPY131685_08', 'INPY131685_09']
P_9999 = ['ITAP138785_01', 'ITAP138785_02', 'ITAP138785_03']
P_6920 = ['ITAP138785_04', 'ITAP138785_05']
P_0561 = ['ITAP138785_06']
P_9983 = ['MALE431085_01CLC', 'MALE431085_02CLC', 'MALE431085_03CLC']

bien_ma_mon_hoc = list(set([
    item for sublist in [P_6352, P_7084, P_9079, P_9831, P_0623, P_3995, P_2151, P_0562,
                         P_3984, P_0309, P_7094, P_2148, P_9153, P_1352, P_6452, P_9999,
                         P_6920, P_0561, P_9983] for item in sublist
]))

sch_problem = Problem(BacktrackingSolver())

morning_slots = list(range(1, 25))  
afternoon_slots = list(range(25, 49)) 
evening_slots = list(range(49, 73)) 

sch_problem.addVariables(bien_ma_mon_hoc, morning_slots + afternoon_slots + evening_slots)



def kiem_tra_trung(*values):
    data = list(values)
    data.sort()
    set_kiem_tra = set()

    for x in data:
        y = x
        while y <= 72:
            y += 18
            set_kiem_tra.add(y)

        phan_con_lai = data[data.index(x) + 1:]
        for v in phan_con_lai:
            if v in set_kiem_tra:
                return False

    return True

sch_problem.addConstraint(AllDifferentConstraint(), bien_ma_mon_hoc)


for group in [P_6352, P_7084, P_9079, P_9831, P_0623, P_3995, P_2151, P_0562, P_3984,
              P_0309, P_7094, P_2148, P_9153, P_1352, P_6452, P_9999, P_6920, P_0561, P_9983]:
    sch_problem.addConstraint(FunctionConstraint(kiem_tra_trung), group)


st.title("Thời Khóa Biểu Nhà Trường")
with st.spinner('Đang giải quyết bài toán...'):
    start = time()
    soln_dts = sch_problem.getSolution()
    elapsed = time() - start


if soln_dts is None:
    st.error("Không tìm thấy giải pháp phù hợp.")
else:
    st.success(f"Đã tìm thấy giải pháp trong {elapsed:.2f} giây.")
    data_sorted = dict(sorted(soln_dts.items(), key=lambda item: item[1], reverse=False))

    st.header("TKB cho từng giáo viên")
    gv_schedule = {}
    for group in [P_6352, P_7084, P_9079, P_9831, P_0623, P_3995, P_2151, P_0562, P_3984, P_0309, P_7094, P_2148, P_9153, P_1352, P_6452, P_9999, P_6920, P_0561, P_9983]:
        gv_key = group[0] 
        for subject in group:
            if subject in data_sorted:
                if gv_key not in gv_schedule:
                    gv_schedule[gv_key] = []
                gv_schedule[gv_key].append((subject, data_sorted[subject]))
    for gv, schedule in gv_schedule.items():
        st.subheader(f"Giáo viên {gv}")
        for subject, slot in schedule:
            buoi = "Sáng" if slot <= 24 else "Chiều" if slot <= 48 else "Tối"
            st.write(f"- Môn {subject}, Phòng {slot}, Buổi {buoi}")

    st.header("TKB cho từng lớp")
    for subject, slot in data_sorted.items():
        buoi = "Sáng" if slot <= 24 else "Chiều" if slot <= 48 else "Tối"
        st.write(f"- Môn {subject}: Phòng {slot}, Buổi {buoi}")

    st.header("TKB từng phòng học cho nhà trường")
    room_schedule = {}
    for subject, slot in data_sorted.items():
        if slot not in room_schedule:
            room_schedule[slot] = []
        room_schedule[slot].append(subject)
    for room, subjects in room_schedule.items():
        buoi = "Sáng" if room <= 24 else "Chiều" if room <= 48 else "Tối"
        st.subheader(f"Phòng {room}, Buổi {buoi}")
        for subject in subjects:
            
            gv_name = None
            for group in [P_6352, P_7084, P_9079, P_9831, P_0623, P_3995, P_2151, P_0562, P_3984, P_0309, P_7094, P_2148, P_9153, P_1352, P_6452, P_9999, P_6920, P_0561, P_9983]:
                if subject in group:
                    gv_name = group[0]
                    break
            st.write(f"- Môn {subject}, Giáo viên {gv_name}")
