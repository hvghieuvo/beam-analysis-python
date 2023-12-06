from typing import Any
import numpy as np
import streamlit as st
from streamlit.hello.utils import show_code
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from io import StringIO, BytesIO
from PIL import Image
import base64
import plotly.express as px

st.set_page_config(page_title="Section Designer", page_icon="🙃", layout = 'wide')
st.markdown("# Section Designer")
st.sidebar.header("Section Designer Tool")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Theory", "Input", "Output"])
with tab1:
    # Hiển thị lý thuyết với đường link đến tài liệu
    st.header('Introduction')
    st.markdown('''<p style="font-size:20px; text-align:justyfy">The analysis of homogenous cross-sections is particularly relevant in structural design, in particular for the design of steel structures, where complex built-up sections are often utilised. Accurate warping independent properties, such as the second moment of area and section moduli, are crucial input for structural analysis and stress verification. Warping dependent properties, such as the Saint-Venant torsion constant and warping constant are essential in the verification of slender steel structures when lateral-torsional buckling is critical.</p>''',unsafe_allow_html=True)
    st.link_button('Click here!','https://sectionproperties.readthedocs.io/en/stable/user_guide/theory.html')

with tab2:
    select = st.selectbox('Cross section type', ('Rectangle', 'Circle','Annulus','C','I'))
    if select == 'Rectangle':
        col1, col2, col3 = st.columns(3, gap='large')
        with col1:
            high = st.number_input(label='Height', min_value=0.00, max_value=None, step=0.01)
            thickness = st.number_input(label='Thickness', min_value=0.00, max_value=None, step=0.01)
            width = st.number_input(label='Width', min_value=0.00, max_value=None, step=0.01)
        with col2:
            max_bending_moment = st.number_input('Maximum bending moment (kNm)', min_value=0.00, max_value=None, step=0.01)
            max_shear_force = st.number_input('Maximum shear force (kN)', min_value=0.00, max_value=None, step=0.01)
            shear_force_at_maximum_moment = st.number_input('Shear force at maximum moment (kN)', min_value=0.00, max_value=None, step=0.01)
            allowable_stress = st.number_input('Allowable stress (N/m^2)', min_value=0.00, max_value=None, step=0.01)
        with col3:
            type_criterion = st.selectbox('Type criterion', ('Tresca', 'von Mises'))
    
    elif select == 'Circle':
        col1_1, col2_1, col3_1 = st.columns(3, gap='large')
        with col1_1:
            R = st.number_input(label="Radius", min_value=0.00, max_value=None, step=0.01)
            thickness = st.number_input(label='Thickness', min_value=0.00, max_value=None, step=0.01)
        with col2_1:
            max_bending_moment = st.number_input('Maximum bending moment (kNm)', min_value=0.00, max_value=None, step=0.01)
            max_shear_force = st.number_input('Maximum shear force (kN)', min_value=0.00, max_value=None, step=0.01)
            shear_force_at_maximum_moment = st.number_input('Shear force at maximum moment (kN)', min_value=0.00, max_value=None, step=0.01)
            allowable_stress = st.number_input('Allowable stress (N/m^2)', min_value=0.00, max_value=None, step=0.01)
        with col3_1:
            type_criterion = st.selectbox('Type criterion', ('Tresca', 'von Mises'))

    elif select == 'Annulus':
        col1_2, col2_2, col3_2 = st.columns(3, gap='large')   
        with col1_2:
            R_in = st.number_input(label='Radius in', min_value=0.00, max_value=None, step=0.01)  
            R_out = st.number_input(label='Radius out', min_value=0.00, max_value=None, step=0.01)
            thickness = st.number_input(label='Thickness', min_value=0.00, max_value=None, step=0.01)
        with col2_2:
            max_bending_moment = st.number_input('Maximum bending moment (kNm)', min_value=0.00, max_value=None, step=0.01)
            max_shear_force = st.number_input('Maximum shear force (kN)', min_value=0.00, max_value=None, step=0.01)
            shear_force_at_maximum_moment = st.number_input('Shear force at maximum moment (kN)', min_value=0.00, max_value=None, step=0.01)
            allowable_stress = st.number_input('Allowable stress (N/m^2)', min_value=0.00, max_value=None, step=0.01)
        with col3_2:
            type_criterion = st.selectbox('Type criterion', ('Tresca', 'von Mises'))

    elif select == 'C':
        st.title('Cross-section C table')
        N0_values=[5, 6.5, 8, 10, 12, 14, '14a', 16, '16a', 18, '18a', 20, '20a', 22, '22a', 24, '24a', 27, 30, 33, 36, 40]
        P_values=[54.2, 65, 77.8, 92, 108, 123, 132, 141, 151, 161, 172, 184, 196, 209, 225, 240, 258, 277, 318, 365, 419, 483]
        h_values=[50, 65, 80, 100, 120, 140, 140, 160, 160, 180, 180, 200, 200, 220, 220, 240, 240, 270, 300, 330, 360, 400]
        b_values=[37, 40, 45, 50, 54, 58, 62, 64, 68, 70, 74, 76, 80, 82, 87, 90, 95, 95, 100, 105, 110, 115]
        d_values=[4.5, 4.5, 4.8, 4.8, 5, 5, 5, 5, 5, 5, 5, 5.2, 5.2, 5.3, 5.3, 5.6, 5.6, 6, 6.5, 7, 7.5, 8]
        t_values=[7, 7.4, 7.4, 7.5, 7.7, 8, 8.5, 8.3, 8.8, 8.7, 9.2, 9, 9.6, 9.6, 10.2, 10, 10.7, 10.5, 11, 11.7, 12.6, 13.5]
        R_values=[6, 6, 6.5, 7, 7.5, 8, 8, 8.5, 8.5, 9, 9, 9.5, 9.5, 10, 10, 10.5, 10.5, 11, 12, 13, 14, 15]
        r_values=[2.5, 2.5, 2.5, 3, 3, 3, 3, 3.5, 3.5, 3.5, 3.5, 4, 4, 4, 4, 4, 4, 4.5, 5, 5, 6, 6]
        S_values=[6.9, 8.28, 9.91, 11.7, 13.7, 15.7, 16.9, 18, 19.3, 20.5, 21.9, 23.4, 25, 26.7, 28.6, 30.6, 32.9, 35.2, 40.5, 46.5, 53.4, 61.5]
        Jx_values=[26.1, 54.5, 99.9, 187, 313, 489, 538, 741, 811, 1080, 1180, 1520, 1660, 2120, 2320, 2900, 3180, 4160, 5810, 7980, 10820, 15220]
        Wx_values=[10.4, 16.8, 25, 37.3, 52.2, 69.8, 76.8, 92.6, 101, 120, 131, 152, 166, 193, 211, 242, 265, 308, 387, 484, 601, 761]
        ix_values=[1.94, 2.57, 3.17, 3.99, 4.78, 5.59, 5.65, 6.42, 6.48, 7.26, 7.33, 8.07, 8.15, 8.91, 9.01, 9.73, 9.84, 10.9, 12, 13.1, 14.2, 15.7]
        Sx_values=[6.36, 10, 14.8, 21, 30.5, 40.7, 44.6, 53.7, 58.5, 69.4, 75.2, 87.8, 95.2, 111, 121, 139, 151, 178, 224, 281, 350, 444]
        Jy_values=[8.41, 11.9, 17.8, 25.6, 34.4, 45.1, 56.6, 62.6, 77.3, 85.6, 104, 113, 137, 151, 186, 208, 254, 262, 327, 410, 513, 642]
        Wy_values=[3.59, 4.58, 5.89, 7.42, 9.01, 10.9, 13, 13.6, 16, 16.9, 19.7, 20.5, 24, 25.4, 29.9, 31.6, 37.2, 37.2, 43.6, 51.8, 61.7, 73.4]
        iy_values=[1.1, 1.2, 1.34, 1.48, 1.58, 1.7, 1.83, 1.87, 2, 2.04, 2.18, 2.2, 2.34, 2.38, 2.55, 2.6, 2.78, 2.78, 2.84, 2.97, 3.1, 3.23]
        Xo_values=[1.36, 1.4, 1.48, 1.55, 1.59, 1.66, 1.84, 1.79, 1.98, 1.95, 2.13, 2.07, 2.27, 2.24, 2.47, 2.42, 2.67, 2.67, 2.52, 2.59, 2.68, 2.75]
        # Chuyển đổi giá trị 'N0' thành chuỗi
        N0_values_str = [str(val) for val in N0_values]
        data = {
            'N0': N0_values_str,
            'P': ['{:.2f}'.format(val) for val in P_values],
            'h': ['{:.2f}'.format(val) for val in h_values],
            'b': ['{:.2f}'.format(val) for val in b_values],
            'd': ['{:.2f}'.format(val) for val in d_values],
            't': ['{:.2f}'.format(val) for val in t_values],
            'R': ['{:.2f}'.format(val) for val in R_values],
            'r': ['{:.2f}'.format(val) for val in r_values],
            'S': ['{:.2f}'.format(val) for val in S_values],
            'Jx': ['{:.2f}'.format(val) for val in Jx_values],
            'Wx': ['{:.2f}'.format(val) for val in Wx_values],
            'ix': ['{:.2f}'.format(val) for val in ix_values],
            'Sx': ['{:.2f}'.format(val) for val in Sx_values],
            'Jy': ['{:.2f}'.format(val) for val in Jy_values],
            'Wy': ['{:.2f}'.format(val) for val in Wy_values],
            'iy': ['{:.2f}'.format(val) for val in iy_values],
            'Xo': ['{:.2f}'.format(val) for val in Xo_values]           
        }
        df = pd.DataFrame(data)        
        st.table(df)
        st.markdown('---')
        
        # Lựa chọn giá trị trong 'N0'
        selected_N0 = st.selectbox("Choose N0", df['N0'].unique())

        # Lọc dữ liệu theo giá trị N0 đã chọn
        selected_rows = df[df['N0'] == selected_N0]
        # Hiển thị thông tin chi tiết
        if not selected_rows.empty:
            st.markdown("Detail:")
            st.write(selected_rows)     
        st.markdown('---')
        col1_2, col2_2, col3_2 = st.columns(3, gap='large')
        with col1_2:
            thickness = st.number_input(label='Thickness', min_value=0.00, max_value=None, step=0.01)
        with col2_2:
            max_bending_moment = st.number_input('Maximum bending moment (kNm)', min_value=0.00, max_value=None, step=0.01)
            max_shear_force = st.number_input('Maximum shear force (kN)', min_value=0.00, max_value=None, step=0.01)
            shear_force_at_maximum_moment = st.number_input('Shear force at maximum moment (kN)', min_value=0.00, max_value=None, step=0.01)
            allowable_stress = st.number_input('Allowable stress (N/m^2)', min_value=0.00, max_value=None, step=0.01)
        with col3_2:
            type_criterion = st.selectbox('Type criterion', ('Tresca', 'von Mises'))

        
                
