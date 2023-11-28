from typing import Any
import numpy as np
import streamlit as st
from streamlit.hello.utils import show_code


st.header("Beam Calculator")

st.set_page_config(page_title="Beam Calculator", page_icon="🙃")
st.markdown("# Beam Calculator")
st.sidebar.header("Beam Calculator Tool")
st.markdown("---")
st.write(
    """
    ### STILL UNDER CONSTRUCTION!!!
    This tool is use to calculate and plot the internal force, shear force and bending moment diagram.
    """
)
st.markdown("---")


def app():
    st.title("Beam Calculator")

    option = st.selectbox(
    'Bạn muốn chọn loại dầm nào',
    ('Dầm console', 'Dầm 2 gối'))