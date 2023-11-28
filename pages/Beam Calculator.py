from typing import Any
import numpy as np
import streamlit as st
from streamlit.hello.utils import show_code
from streamlit_option_menu import option_menu 

st.set_page_config(page_title='Đề 1',layout='wide')

def app():
    st.title('Tính toán dầm')
    selected = option_menu(None, ["Lý thuyết", "Nhập thông số đầu vào","Kết quả"],
    default_index=0, orientation="horizontal",styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "20px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "blue"},
    })
    selected
    if selected == "Lý thuyết":
        