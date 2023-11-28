from typing import Any
import numpy as np
import streamlit as st
from streamlit.hello.utils import show_code
from streamlit_option_menu import option_menu 

st.set_page_config(page_title="Beam Calculator", page_icon="🙃")
st.markdown("# Beam Calculator")
st.sidebar.header("Beam Calculator Tool")
st.markdown("---")
def app():
    st.title('Tính toán dầm')
    selected = option_menu(None, ["Lý thuyết", "Nhập thông số đầu vào"],
    default_index=0, orientation="horizontal",styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "20px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "blue"},
    })
    selected

    length = st.slider('Chiều dài của dầm?', 0,100)
    

    if selected == "Lý thuyết":
        st.write('hehehe')

    if selected == "Nhập thông số đầu vào":
        col1, col2 = st.columns([1,2])
        with col1:
            st.subheader('Chọn loại dầm')
            dam_console = st.checkbox('Dầm console')
            if dam_console:
                st.write('Nhập chiều dài: ', length)
            dam_2goi = st.checkbox('Dầm 2 gối')
            if dam_2goi: