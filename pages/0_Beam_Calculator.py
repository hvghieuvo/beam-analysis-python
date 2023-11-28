from typing import Any
import numpy as np
import streamlit as st
from streamlit.hello.utils import show_code
from streamlit_option_menu import option_menu 

st.set_page_config(page_title="Beam Calculator", page_icon="🙃")
st.markdown("# Beam Calculator")
st.sidebar.header("Beam Calculator Tool")
st.markdown("---")

with st.columns:
    st.selectbox('Hãy chọn loại dầm',
             ('Dầm console', 'Dầm 2 gối'))
    length = st.slider('Chiều dài dầm: ', 0,100)