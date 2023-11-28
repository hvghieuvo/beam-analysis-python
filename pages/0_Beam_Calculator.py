from typing import Any
import numpy as np
import streamlit as st
from streamlit.hello.utils import show_code
from streamlit_option_menu import option_menu 

st.set_page_config(page_title="Beam Calculator", page_icon="🙃")
st.markdown("# Beam Calculator")
st.sidebar.header("Beam Calculator Tool")
st.markdown("---")
tab1, tab2 = st.tabs(["Lý thuyết", "Input"])
with tab1:
    st.header('Lý thuyết')
    st.markdown('''<p style="font-size:20px; text-align:justyfy">A brief overview of the engineering theory and conventions used in this program are illustrated below. Theory is adapted from the Hibbeler textbook [2]. A more rigorous overview of the basic theory behind statically determinate structures is presented in the beambending package documentation.</p>''',unsafe_allow_html=True)
    st.link_button('Ấn để biết thêm chi tiết','https://indeterminatebeam.readthedocs.io/en/main/theory.html?fbclid=IwAR18lJpYVJm1MnqkVdXydhA0eLWQwSmCV4w6VzKAIK5dueK9zq-_gYrxMy0')



def app():
    st.title('Tính toán dầm')
    selected = option_menu(None, ["Lý thuyết", "Input"],
    default_index=0, orientation="horizontal",styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "20px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "blue"},
    })
    selected
    if selected == "Lý thuyết":
        st.write('hehehe')

    if selected == "Input":
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Chọn loại dầm')
            select = st.selectbox('Hãy chọn loại dầm',
             ('Dầm console', 'Dầm 2 gối'))
            if select == 'Dầm console':
                x = st.slider('Chọn chiều dài của dầm từ 0 - 100?', min_value=0, max_value=100, step=0)
                length_1 = st.write('Chiều dài của dầm là: ', x)
                a = st.selectbox('Số lực muốn chọn cho dằm', ('2'), ('3'))
                if a == '2':
                    luc_1 = st.slider('Vị trí dặt lực 1?', 0,100)
                    luc_2 = st.slider('Vị trí dặt lực 2?', 0,100)
                else:
                    luc_1 = st.slider('Vị trí dặt lực 1?', 0,100)
                    luc_2 = st.slider('Vị trí dặt lực 2?', 0,100)
                    luc_3 = st.slider('Vị trí dặt lực 3?', 0,100)
