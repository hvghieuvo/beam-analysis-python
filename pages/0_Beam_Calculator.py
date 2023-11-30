from typing import Any
import numpy as np
import streamlit as st
from streamlit.hello.utils import show_code
from streamlit_option_menu import option_menu 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Beam Calculator", page_icon="🙃")
st.markdown("# Beam Calculator")
st.sidebar.header("Beam Calculator Tool")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Theory", "Input", "Output"])


with tab1:
    st.markdown('''<p style="font-size:20px; text-align:justyfy">A brief overview of the engineering theory and conventions used in this program are illustrated below. Theory is adapted from the Hibbeler textbook [2]. A more rigorous overview of the basic theory behind statically determinate structures is presented in the beambending package documentation.</p>''',unsafe_allow_html=True)
    st.link_button('Click here!','https://indeterminatebeam.readthedocs.io/en/main/theory.html?fbclid=IwAR18lJpYVJm1MnqkVdXydhA0eLWQwSmCV4w6VzKAIK5dueK9zq-_gYrxMy0')


with tab2:
    select = st.selectbox('Beam type',
    ('Console', 'Beam with 2 supports'))
    if select == 'Console':
        length = st.number_input('Length (in m)',min_value=0,max_value=None,step=1, placeholder='Type a number...')
            
        forces = []
        num_forces = st.number_input('Number of forces', min_value=0, step=1, value=0)
        for i in range(1, num_forces + 1):
            st.write(f'Force {i}')
            position_of_forces = st.number_input(f"Position of force {i} (in m)", min_value=0, max_value=length, step=1)
            magnitude_of_forces = st.number_input(f"Magnitude of force {i} (in kN)",)
            
            forces.append({
                'position': position_of_forces,
                'magnitude': magnitude_of_forces
            })

        distributed_loads = []
        num_distributed_loads = st.number_input('Number of distributed loads', min_value=0, step=1, value=0)

        for i in range(1, num_distributed_loads + 1):
            st.write(f'Distributed Force {i}')
            start_point = st.number_input(f'Start point {i} (in m)', min_value=0, max_value=length, step=1)
            end_point = st.number_input(f'End point {i} (in m)', min_value=start_point, max_value=length, step=1)
            magnitude_of_Distributed = st.number_input(f'Magnitude of distributed load {i} (in kN)')

            distributed_loads.append({
                'start_point': start_point,
                'end_point': end_point,
                'magnitude': magnitude_of_Distributed
            })
        
        moments = []
        num_moments = st.number_input('Number of moments', min_value=0, step=1, value=0)

        for i in range(1, num_moments + 1):
            st.write(f'Moment {i}')
            position_of_moment = st.number_input(f'Position of moment {i} (in m)', min_value=0,max_value=length, step=1)
            magnitude_of_moment = st.number_input(f'Magnitude of moment {i} (in kN/m^2)',)

            moments.append({
                'position': position_of_moment,
                'magnitude': magnitude_of_moment
            })
        
    if select == 'Beam with 2 supports':
        length_1 = st.number_input('Length (in m)',min_value=1,max_value=None,step=1, placeholder='Type a number...')
        pinned_1 = st.slider("Position of pinned 1 (in m)", 0, length_1, None)
        pinned_2 = st.slider("Position of pinned 2 (in m)", 0, length_1, None)
        
        forces_1 = []
        num_forces_1 = st.number_input('Number of forces', min_value=0, step=1, value=0)
        for i in range(1, num_forces_1 + 1):
            st.write(f'Force {i}')
            position_of_forces_1 = st.number_input(f"Position of force {i} (in m)", min_value=0, max_value=length_1, step=1)
            magnitude_of_forces_1 = st.number_input(f"Magnitude of force {i} (in kN)",)
            
            forces_1.append({
                'position': position_of_forces_1,
                'magnitude': magnitude_of_forces_1
            })

        distributed_loads_1 = []
        num_distributed_loads_1 = st.number_input('Number of distributed loads', min_value=0, step=1, value=0)

        for i in range(1, num_distributed_loads_1 + 1):
            st.write(f'Distributed Force {i}')
            start_point_1 = st.number_input(f'Start point {i} (in m)', min_value=0, max_value=length_1, step=1)
            end_point_1 = st.number_input(f'End point {i} (in m)', min_value=0, max_value=length_1, step=1)
            magnitude_of_Distributed_1 = st.number_input(f'Magnitude of distristreabuted load {i} (in kN)')

            distributed_loads_1.append({
                'start_point': start_point_1,
                'end_point': end_point_1,
                'magnitude': magnitude_of_Distributed_1
            })
        
        moments_1 = []
        num_moments_1 = st.number_input('Number of moments', min_value=0, step=1, value=0)

        for i in range(1, num_moments_1 + 1):
            st.write(f'Moment {i}')
            position_of_moment_1 = st.number_input(f'Position of moment {i} (in m)', min_value=0,max_value=length_1, step=1)
            magnitude_of_moment_1 = st.number_input(f'Magnitude of moment {i} (in kN/m**2)',)

            moments_1.append({
                'position': position_of_moment_1,
                'magnitude': magnitude_of_moment_1
                 })

def fig_to_bytes(fig):
    with BytesIO() as buffer:
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        return buffer.getvalue()      
with tab3:
    if select == 'Console':
        fig, ax = plt.subplots(figsize=(8, 6))
        image_data = fig_to_bytes(fig)
        st.image(image_data, caption='Figure 1')
    elif select == 'Beam with 2 supports':
        fig, ax = plt.subplots(figsize=(8, 6))
        image_data = fig_to_bytes(fig)
        st.image(image_data, caption='Figure 1')
    