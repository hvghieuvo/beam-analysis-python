from typing import Any
import numpy as np
import streamlit as st
from streamlit.hello.utils import show_code

st.set_page_config(page_title='Đề 1',layout='wide')
st.markdown("---")

st.sidebar.header('Đề 1')

st.title('Tính toán dầm')
option = st.selectbox(
    'Hãy chọn loại dầm cần tính', 
    ('Dầm console','Dầm 2 gối'))
st.write('Lựa chọn là: ', option)
