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
    st.header('Theory')
    st.markdown('''<p style="font-size:20px; text-align:justyfy">A brief overview of the engineering theory and conventions used in this program are illustrated below. Theory is adapted from the Hibbeler textbook [2]. A more rigorous overview of the basic theory behind statically determinate structures is presented in the beambending package documentation.</p>''',unsafe_allow_html=True)
    st.link_button('Click here!','https://indeterminatebeam.readthedocs.io/en/main/theory.html?fbclid=IwAR18lJpYVJm1MnqkVdXydhA0eLWQwSmCV4w6VzKAIK5dueK9zq-_gYrxMy0')
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Chọn loại dầm')
        select = st.selectbox('Chọn loại dầm',
        ('Dầm console', 'Dầm 2 gối'))
        if select == 'Dầm console':
            length = st.number_input('Length of beam?',min_value=0,max_value=None,step=1, placeholder='Type a number...')
            num_force = st.number_input('Amount of force want to add?', min_value=0,max_value=None,step=1, placeholder='Type a number...')
            if num_force > 0:
                st.write(f"Equivalent forces:")
            for i in range(1, num_forces + 1):
                force_position = st.number_input(f'Force {i} - Vị trí lực:', min_value=0, max_value=length, step=1, key=f'position_{i}')
                force_magnitude = st.number_input(f'Force {i} - Độ lớn lực:', min_value=0, max_value=None, step=1, key=f'magnitude_{i}')

                st.write(f"Force {i}: Position - {force_position}, Magnitude - {force_magnitude}")

            if __name__ == '__main__':
                main()
                
            distributed_load = st.number_input('Amount of distributed load want to add?', min_value=0,max_value=None,step=1, placeholder='Type a number...')
            moment = st.number_input('Magnitude of moment',min_value=0,max_value=None,step=1, placeholder='Type a number...')
                

                        
