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
            length = st.number_input('Length of beam?', value=None, placeholder='Type a number...')
            point_load = st.number_input('Amount of force want to add?', value=int, placeholder='Type a number...')


                        
