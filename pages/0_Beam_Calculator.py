from typing import Any
import numpy as np
import streamlit as st
from streamlit.hello.utils import show_code
from streamlit_option_menu import option_menu 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
# from beam import create_beam, add_load, add_sp, plot_diagram

# Kiểm tra nếu 'console_forces' không tồn tại trong session state thì khởi tạo
if 'console_forces' not in st.session_state:
    st.session_state.console_forces = []

# Kiểm tra nếu 'beam_forces' không tồn tại trong session state thì khởi tạo
if 'beam_forces' not in st.session_state:
    st.session_state.beam_forces = []

if 'advanced_forces' not in st.session_state:
    st.session_state.advanced_forces = []

# Biến trạng thái để kiểm soát việc hiển thị và tính toán
if 'solve_clicked' not in st.session_state:
    st.session_state.solve_clicked = False

st.set_page_config(page_title="Beam Calculator", page_icon="🙃",layout = 'wide')
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
    select = st.selectbox('Beam type', ('Console', 'Beam with 2 supports','Advanced'))
    st.markdown('---')
    # Chọn Console
    if select == 'Console':
        col1, col2, col3 = st.columns(3, gap='large')
        # Tạo hộp để nhập số liệu
        with col1: 
            length = st.number_input(label='Length (m)', min_value=0.00, max_value=None, step=0.01)
            st.markdown('---')
            
            fixed_type = st.selectbox('Fixed position', ('Fixed left end', 'Fixed right end'))
            #Thêm ngàm trái hoặc phải
            # if fixed_type == "Fixed left end":
            #     add_sp(0, "fixed")
            # else: add_sp(length, "fixed")
            
        with col2:
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
        with col3: 
            st.write('Added forces:')
            for idx, force in enumerate(st.session_state.console_forces, start=1):
                delete_checkbox = st.checkbox(f"Delete load {idx}")
                st.write(f"{idx}. Type load is {force['Type Load']}, Magnitude: {force['Magnitude']} (kN)" +
                    (f", Position: {force['Position']} (m)" if force['Type Load'] in ['Point load', 'Moment'] else "") +
                    (f", Start Position: {force['Start Position']} (m)" if 'Start Position' in force else "") +
                    (f", End Position: {force['End Position']} (m)" if 'End Position' in force else ""))
                if delete_checkbox:
                    st.session_state.console_forces.pop(idx - 1)
            st.button('Quick solve')



        st.image('images/console.jpg', caption='Console')
        st.markdown('---')
        if st.button('Solve'):
            st.session_state.solve_clicked = True
            
    # Beam with 2 supports
    elif select == 'Beam with 2 supports':
        col1_1, col1_2, col1_3, col1_4 = st.columns(4, gap='large')
        
        with col1_1:
            length_1 = st.number_input(label='Length (m)', min_value=1.00, max_value=None, step=0.01)
            st.markdown('---')
            support_type_right = st.selectbox('Support type right', ('Pin', 'Roller'))
            support_type_left = st.selectbox('Support type left', ('Pin', 'Roller'))
        
        with col1_2:
            sup_1 = st.slider("Position of support 1 (m)", 0.00, length_1, None)
            sup_2 = st.slider("Position of support 2 (m)", 0.00, length_1, None)
            
        with col1_3:
            type_load_1 = st.selectbox('Type forces', ('Point load', 'Distributed load', 'Moment'))
            st.markdown('---')
            if type_load_1 in ['Point load', 'Moment']:
                magnitude_1 = st.number_input('Magnitude (kN)', min_value=0.00, step=0.01)
                position_1 = st.slider('Position (m)', min_value=0.00, max_value=length_1, step=0.01)
                if st.button('Add'):
                    st.session_state.beam_forces.append({'Type Load': type_load_1, 'Magnitude': magnitude_1, 'Position': position_1})
            
            elif type_load_1 == 'Distributed load':
                magnitude_1 = st.number_input('Magnitude (kN)', min_value=0.00, step=0.01)
                start_point_1 = st.slider('Start position (m)', min_value=0.00, max_value=None, step=0.01)
                end_point_1 = st.slider('End position (m)', min_value=0.00, max_value=length_1, step=0.01)
                if st.button('Add'):
                    st.session_state.beam_forces.append({'Type Load': type_load_1, 'Magnitude': magnitude_1, 'Start Position': start_point_1, 'End Position': end_point_1})
            
        with col1_4:
            st.write('Added forces:')
            for idx, force in enumerate(st.session_state.beam_forces, start=1):
                delete_checkbox_1 = st.checkbox(f"Delete load {idx}")
                st.write(f"{idx}. Type load is {force['Type Load']}, Magnitude: {force['Magnitude']} (kN)" +
                        (f", Position: {force['Position']} (m)" if force['Type Load'] in ['Point load', 'Moment'] else "") +
                        (f", Start Position: {force['Start Position']} (m)" if 'Start Position' in force else "") +
                        (f", End Position: {force['End Position']} (m)" if 'End Position' in force else ""))
                if delete_checkbox_1:
                    st.session_state.beam_forces.pop(idx - 1)
            st.button('Quick solve')
        
        st.image('images/2sup.jpg', caption='Beam with 2 supports')   
        st.markdown('---')
        if st.button('Solve'):
            st.session_state.solve_clicked = True
            
            #Giải và plot đồ thị
            # plot_diagram(1)
            
    elif select == 'Advanced':
        col2_1, col2_2, col2_3, col2_4 = st.columns(4, gap='large')
        with col2_1:
            length_2 = st.number_input(label='Length (m)', min_value=1.00, max_value=None, step=0.01)
            st.markdown('---')
            data_df = pd.DataFrame(
                {
                    "category": [
                        "Pin",
                        "Roller",
                        "Fixed",
                    ],
                }
            )

            st.data_editor(
                data_df,
                column_config={
                    "category": st.column_config.SelectboxColumn(
                        "Support type",
                        help="The category of the app",
                        width="medium",
                        options=[
                            "Pin",
                            "Roller",
                            "Fixed"
                        ],
                        required=True,
                    )
                },
                hide_index=True,
                num_rows="dynamic",
            )
            
        with col2_2:
            support_1_position = st.slider('Position of support 1', 0.00, length_2,None)
            support_2_position = st.slider('Position of support 2', 0.00, length_2,None)
            support_3_position = st.slider('Position of support 3', 0.00, length_2,None)
        with col2_3:
            type_load_2 = st.selectbox('Type forces', ('Point load', 'Distributed load', 'Moment'))
            st.markdown('---')
            if type_load_2 in ['Point load', 'Moment']:
                magnitude_2 = st.number_input('Magnitude (kN)', min_value=0.00, step=0.01)
                position_2 = st.slider('Position (m)', min_value=0.00, max_value=length_2, step=0.01)
                if st.button('Add'):
                    st.session_state.advanced_forces.append({'Type Load': type_load_2, 'Magnitude': magnitude_2, 'Position': position_2})
            
            elif type_load_2 == 'Distributed load':
                magnitude_2 = st.number_input('Magnitude (kN)', min_value=0.00, step=0.01)
                start_point_2 = st.slider('Start position (m)', min_value=0.00, max_value=None, step=0.01)
                end_point_2 = st.slider('End position (m)', min_value=0.00, max_value=length_2, step=0.01)
                if st.button('Add'):
                    st.session_state.advanced_forces.append({'Type Load': type_load_2, 'Magnitude': magnitude_2, 'Start Position': start_point_2, 'End Position': end_point_1})
            
        with col2_4:
            st.write('Added forces:')
            for idx, force in enumerate(st.session_state.advanced_forces, start=1):
                delete_checkbox_2= st.checkbox(f"Delete load {idx}")
                st.write(f"{idx}. Type load is {force['Type Load']}, Magnitude: {force['Magnitude']} (kN)" +
                        (f", Position: {force['Position']} (m)" if force['Type Load'] in ['Point load', 'Moment'] else "") +
                        (f", Start Position: {force['Start Position']} (m)" if 'Start Position' in force else "") +
                        (f", End Position: {force['End Position']} (m)" if 'End Position' in force else ""))
                if delete_checkbox_2:
                    st.session_state.advanced_forces.pop(idx - 1) 
            if st.button('Quick Solve'):
                st.session_state.quick_solve_clicked = True
                #Giải và plot đồ thị
                # plot_diagram(0)
        
                    
        st.image('images/advanced.jpg', caption='Beam with many supports')
        st.markdown('---')
        if st.button('Solve'):
            st.session_state.solve_clicked = True
            #Giải và plot đồ thị
            # plot_diagram(1)
            
with tab3:
    st.image('images/fig_reac.png', caption='Reaction force diagram')
    st.divider()
    
    st.image('images/fig_shear.png', caption='Shear force diagram')
    st.divider()

    st.image('images/fig_normal.png', caption='Normal force diagram')
    st.divider()

    st.image('images/fig_moment.png', caption='Bending moment diagram')
    st.divider()

