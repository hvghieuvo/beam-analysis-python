from typing import Any
import numpy as np
import streamlit as st
from streamlit.hello.utils import show_code
from streamlit_option_menu import option_menu 
import matplotlib.pyplot as plt
import matplotlib.animation as animation

st.set_page_config(page_title="Beam Calculator", page_icon="🙃")
st.markdown("# Beam Calculator")
st.sidebar.header("Beam Calculator Tool")
st.markdown("---")
tab1, tab2 = st.tabs(["Theory", "Input"])
with tab1:
    st.markdown('''<p style="font-size:20px; text-align:justyfy">A brief overview of the engineering theory and conventions used in this program are illustrated below. Theory is adapted from the Hibbeler textbook [2]. A more rigorous overview of the basic theory behind statically determinate structures is presented in the beambending package documentation.</p>''',unsafe_allow_html=True)
    st.link_button('Click here!','https://indeterminatebeam.readthedocs.io/en/main/theory.html?fbclid=IwAR18lJpYVJm1MnqkVdXydhA0eLWQwSmCV4w6VzKAIK5dueK9zq-_gYrxMy0')
with tab2:
    select = st.selectbox('Beam type',
    ('Console', 'Dầm 2 gối'))
    if select == 'Console':
        length = st.number_input('Length',min_value=0,max_value=None,step=1, placeholder='Type a number...')
            
        forces = []
        num_forces = st.number_input('Number of forces', min_value=0, step=1, value=0)
        for i in range(1, num_forces + 1):
            st.write(f'Force {i}')
            position_of_forces = st.number_input(f"Position of force {i}", min_value=0, max_value=length, step=1)
            magnitude_of_forces = st.number_input(f"Magnitude of force {i}",)
            
            forces.append({
                'position': position_of_forces,
                'magnitude': magnitude_of_forces
            })

        distributed_loads = []
        num_distributed_loads = st.number_input('Number of distributed loads', min_value=0, step=1, value=0)

        for i in range(1, num_distributed_loads + 1):
            st.write(f'Distributed Force {i}')
            start_point = st.number_input(f'Start point {i}', min_value=0, max_value=length, step=1)
            end_point = st.number_input(f'End point {i}', min_value=start_point, max_value=length, step=1)
            magnitude_of_Distributed = st.number_input(f'Magnitude of distributed load {i}')

            distributed_loads.append({
                'start_point': start_point,
                'end_point': end_point,
                'magnitude': magnitude_of_Distributed
            })
        
        moments = []
        num_moments = st.number_input('Number of moments', min_value=0, step=1, value=0)

        for i in range(1, num_moments + 1):
            st.write(f'Moment {i}')
            position_of_moment = st.number_input(f'Position of moment {i}', min_value=0,max_value=length, step=1)
            magnitude_of_moment = st.number_input(f'Magnitude of moment {i}',)

            moments.append({
                'position': position_of_moment,
                'magnitude': magnitude_of_moment
            })
    


            
            

                        
