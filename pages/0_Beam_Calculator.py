from typing import Any
import numpy as np
import streamlit as st
from streamlit.hello.utils import show_code
from streamlit_option_menu import option_menu 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from io import BytesIO
from beam import create_beam, add_sp, add_load, plot_diagram

# Kiểm tra nếu 'console_forces' không tồn tại trong session state thì khởi tạo
if 'console_forces' not in st.session_state:
    st.session_state.console_forces = []

# Kiểm tra nếu 'beam_forces' không tồn tại trong session state thì khởi tạo
if 'beam_forces' not in st.session_state:
    st.session_state.beam_forces = []

# Biến trạng thái để kiểm soát việc hiển thị và tính toán
if 'solve_clicked' not in st.session_state:
    st.session_state.solve_clicked = False

st.set_page_config(page_title="Beam Calculator", page_icon="🙃")
st.markdown("# Beam Calculator")
st.sidebar.header("Beam Calculator Tool")
st.markdown("---")

# Tạo các tab
tab1, tab2, tab3 = st.tabs(["Theory", "Input", "Output"])

# Tab về lý thuyết
with tab1:
    # Hiển thị lý thuyết với đường link đến tài liệu
    st.markdown('''<p style="font-size:20px; text-align:justyfy">A brief overview of the engineering theory and conventions used in this program are illustrated below. Theory is adapted from the Hibbeler textbook [2]. A more rigorous overview of the basic theory behind statically determinate structures is presented in the beambending package documentation.</p>''',unsafe_allow_html=True)
    st.link_button('Click here!','https://indeterminatebeam.readthedocs.io/en/main/theory.html?fbclid=IwAR18lJpYVJm1MnqkVdXydhA0eLWQwSmCV4w6VzKAIK5dueK9zq-_gYrxMy0')

# Tab nhập liệu
added_forces=[]
with tab2:
    # Tab nhập liệu
    select = st.selectbox('Beam type', ('Console', 'Beam with 2 supports'))

    # Chọn Console
    if select == 'Console':
        # Tạo hộp để nhập số liệu
        length = st.number_input(label='Length (m)', min_value=0.00, max_value=None, step=0.01)
        type_load = st.selectbox('Type forces', ('Point load', 'Distributed load', 'Moment'))
        if type_load in ['Point load', 'Moment']:
            magnitude = st.number_input('Magnitude (kN)', min_value=0.00, step=0.01)
            position = st.number_input('Position (m)', min_value=0.00, max_value=length, step=0.01)
            if st.button('Add'):
                st.session_state.console_forces.append({'Type Load': type_load, 'Magnitude': magnitude, 'Position': position})
        
        elif type_load == 'Distributed load':
            # Vừa tạo hộp nhập số liệu, vừa tạo slider
            magnitude = st.number_input('Magnitude (kN)', min_value=0.00, step=0.01)
            start_point = st.number_input('Start position (m)', min_value=0.00, max_value=None, step=0.01)
            end_point = st.number_input('End position (m)', min_value=0.00, max_value=length, step=0.01)
            if st.button('Add'):
                st.session_state.console_forces.append({'Type Load': type_load, 'Magnitude': magnitude, 'Start Position': start_point, 'End Position': end_point})
        
        # Hiển thị các lực đã thêm vào (Console)
        st.markdown('---')
        st.write('Added forces:')
        for idx, force in enumerate(st.session_state.console_forces, start=1):
            delete_checkbox = st.checkbox(f"Delete load {idx}")
            st.write(f"{idx}. Type load is {force['Type Load']}, Magnitude: {force['Magnitude']} (kN)" +
                 (f", Position: {force['Position']} (m)" if force['Type Load'] in ['Point load', 'Moment'] else "") +
                 (f", Start Position: {force['Start Position']} (m)" if 'Start Position' in force else "") +
                 (f", End Position: {force['End Position']} (m)" if 'End Position' in force else ""))
            if delete_checkbox:
                st.session_state.console_forces.pop(idx - 1)
        st.markdown('---')
        if st.button('Solve'):
            st.session_state.solve_clicked = True

    # Beam with 2 supports
    elif select == 'Beam with 2 supports':
        length_1 = st.number_input(label='Length (m)', min_value=1.00, max_value=None, step=0.01)
        pinned_1 = st.slider("Position of pinned 1 (m)", 0.00, length_1, None)
        pinned_2 = st.slider("Position of pinned 2 (m)", 0.00, length_1, None)
        type_load_1 = st.selectbox('Type forces', ('Point load', 'Distributed load', 'Moment'))
        
        if type_load_1 in ['Point load', 'Moment']:
            magnitude_1 = st.number_input('Magnitude (kN)', min_value=0.00, step=0.01)
            position_1 = st.number_input('Position (m)', min_value=0.00, max_value=length_1, step=0.01)
            if st.button('Add'):
                st.session_state.beam_forces.append({'Type Load': type_load_1, 'Magnitude': magnitude_1, 'Position': position_1})
        
        elif type_load_1 == 'Distributed load':
            magnitude_1 = st.number_input('Magnitude (kN)', min_value=0.00, step=0.01)
            start_point_1 = st.number_input('Start position (m)', min_value=0.00, max_value=None, step=0.01)
            end_point_1 = st.number_input('End position (m)', min_value=0.00, max_value=length_1, step=0.01)
            if st.button('Add'):
                st.session_state.beam_forces.append({'Type Load': type_load_1, 'Magnitude': magnitude_1, 'Start Position': start_point_1, 'End Position': end_point_1})
        
        
        st.markdown('---')
        st.write('Added forces:')
        for idx, force in enumerate(st.session_state.beam_forces, start=1):
            delete_checkbox_1 = st.checkbox(f"Delete load {idx}")
            st.write(f"{idx}. Type load is {force['Type Load']}, Magnitude: {force['Magnitude']} (kN)" +
                    (f", Position: {force['Position']} (m)" if force['Type Load'] in ['Point load', 'Moment'] else "") +
                    (f", Start Position: {force['Start Position']} (m)" if 'Start Position' in force else "") +
                    (f", End Position: {force['End Position']} (m)" if 'End Position' in force else ""))
            if delete_checkbox_1:
                st.session_state.beam_forces.pop(idx - 1)
        st.markdown('---')
        if st.button('Solve'):
            st.session_state.solve_clicked = True
with tab3:
    x = np.linspace(0, 10, 100)
    y = np.sin(x)   
    st.subheader("Problem")
    plt.plot(x, y)
    plt.title('Image 1')
    st.pyplot(plt)
    
    
    st.subheader("Axial Force")
    plt.plot(x, y)
    plt.title('Axial Force')
    st.pyplot(plt)

    st.subheader("Shear Force")
    plt.plot(x, y)
    plt.title('Shear Force')
    st.pyplot(plt)

    st.subheader("Bending Moment")
    plt.plot(x, y)
    plt.title('Bending Moment')
    st.pyplot(plt)