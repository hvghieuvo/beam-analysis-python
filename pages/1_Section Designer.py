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
import math
import sys
from section import hinhchunhat, plot_rec, hinhtron, plot_circle, hinhvanhkhan, plot_annulus, hinh_I_C, plot_C, plot_I

if 'solve_clicked' not in st.session_state:
    st.session_state.solve_clicked = False
    
Sx, Sy, Jx, Jy, Wx, Wy, sigmamax, sigmamin, sigmatd, taumax, tau = None, None, None, None, None, None, None, None, None, None, None

def read_output_file(file_path="output.txt"):
    max_bm = max_sf = sf_at_max_bm = None
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
            max_bm = float(lines[0].split(":")[1].strip())
            max_sf = float(lines[1].split(":")[1].strip())
            sf_at_max_bm = float(lines[2].split(":")[1].strip().split("m")[0].strip())
    except FileNotFoundError:
        st.warning(f"File '{file_path}' not found.")
    except Exception as e:
        st.error(f"Error reading file: {e}")

    return max_bm, max_sf, sf_at_max_bm

st.set_page_config(page_title="Section Designer", page_icon="🙃", layout = 'wide')
st.markdown("# Section Designer")
st.sidebar.header("Section Designer Tool")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Theory", "Implement", "Output"])
with tab1:
    # Hiển thị lý thuyết với đường link đến tài liệu
    st.header('Introduction')
    st.markdown('''<p style="font-size:20px; text-align:justyfy">The analysis of homogenous cross-sections is particularly relevant in structural design, in particular for the design of steel structures, where complex built-up sections are often utilised. Accurate warping independent properties, such as the second moment of area and section moduli, are crucial input for structural analysis and stress verification. Warping dependent properties, such as the Saint-Venant torsion constant and warping constant are essential in the verification of slender steel structures when lateral-torsional buckling is critical.</p>''',unsafe_allow_html=True)
    st.link_button('Click here!','https://sectionproperties.readthedocs.io/en/stable/user_guide/theory.html')

with tab2:
    select = st.selectbox('Cross section type', ('Rectangle', 'Circle','Annulus','C shape','I shape'))
    
#============================= Hình chữ nhật #=============================
    if select == 'Rectangle':
        col1, col2, col3 = st.columns(3, gap='large')
        with col1:
            height = st.number_input(label='Height (m)', min_value=0.00, step=0.01)
            thickness = st.number_input(label='Thickness (m)', min_value=0.00, step=0.01)
            width = st.number_input(label='Width (m)', min_value=0.00, step=0.01)
            st.divider()
            input_method = st.selectbox('Choose input method', ('Manual', 'From file'))
        with col2:
            
            if input_method == "Manual":
                max_bending_moment = st.number_input('Maximum bending moment (kNm)', step=0.01)
                max_shear_force = st.number_input('Maximum shear force (kN)', step=0.01)
                shear_force_at_maximum_moment = st.number_input('Shear force at maximum moment (kN)', step=0.01)
                # sigma_t = st.number_input('Allowable tensile stress (N/m^2)', step=0.01)
                
            elif input_method == "From file":
                max_bm, max_sf, sf_at_max_bm = read_output_file()
                if max_bm != None and max_sf != None and sf_at_max_bm != None:
                    max_bending_moment = max_bm
                    max_shear_force = max_sf
                    shear_force_at_maximum_moment = sf_at_max_bm
                    st.success('Import data from file success!', icon="✅")
                    st.write(f"Maximum bending moment (kNm): {max_bm}")
                    st.write(f"Maximum shear force (kN): {max_sf}")
                    st.write(f"Shear force at maximum moment (kN): {sf_at_max_bm}")
                    # sigma = st.number_input('Allowable stress (N/m^2)', step=0.01)
                else:
                    st.error('Error! Something not right', icon="🚨")
                    
            sigma_t = st.number_input('Allowable tensile stress (N/m^2)', step=0.01)
            sigma_c = st.number_input('Allowable compress stress (N/m^2)', step=0.01)
            
        with col3:
            type_criterion = st.selectbox('Type criterion', ('Tresca', 'von Mises'))
            
            #==================== Button solve rectangle #====================
            if st.button("Clear result", type="primary"):
                st.session_state.solve_clicked = False
                
            if st.button('Analysis'):
                st.session_state.solve_clicked = True
                
                st.write(f"Maximum bending moment (kNm): {max_bending_moment}")
                st.write(f"Maximum shear force (kN): {max_shear_force}")
                st.write(f"Shear force at maximum moment (kN): {shear_force_at_maximum_moment}")
                
                try:
                    if type_criterion == "Tresca":
                        tau = sigma_t/2
                    elif type_criterion == "von Mises":
                        tau = sigma_t/math.sqrt(3)
                        
                    Sx, Sy, Jx, Jy, Wx, Wy, sigmamin, sigmamax, taumax = hinhchunhat(width, height, max_bending_moment, max_shear_force)
                    plot_rec(width, height, shear_force_at_maximum_moment, sigmamin, sigmamax, taumax)
                except Exception as error:
                    st.error('Error! Something not right', icon="🚨")
                    st.write(f"An exception occurred: {type(error).__name__} {error}")
                else:
                    st.success('Analysis success!', icon="✅")
                
        st.divider()
        
        output1, output2 = st.columns(2, gap='large')
        with output1:
            if st.session_state.solve_clicked:
                try:
                    st.header("Result:")
                    st.write("")
                    
                    st.write(f"Maximum bending moment (kNm): {max_bending_moment}")
                    st.write(f"Maximum shear force (kN): {max_shear_force}")
                    st.write(f"Shear force at maximum moment (kN): {shear_force_at_maximum_moment}")
                    
                    st.write(f'Static moment Sx: {Sx}')
                    st.write(f'Static moment Sy: {Sy}')
                    st.write(f'Moment of inertia Jx: {Jx}')
                    st.write(f'Moment of inertia Jy: {Jy}')
                    st.write(f'Bending moment Wx: {Wx}')
                    st.write(f'Bending moment Wy: {Wy}')
                    st.write(f'Principal stress sigma_max: {sigmamax}')
                    st.write(f'Maximun shear stress on the section: {taumax}')
                    if sigmamax <= sigma_t:
                        # st.write('Ductile (Durable) boundary layer')
                        st.success('Boundary layer satisfying strength', icon="✅")
                    else:
                        # st.write('Brittle (Not Durable) boundary layer')
                        st.error('Boundary layer NOT satisfying strength', icon="🚨")
                    if taumax <= tau:
                        # st.write('Ductile (Durable) neutral layer')
                        st.success('Neutral layer satisfying strength', icon="✅")
                    else:
                        # st.write('Brittle (Not Durable) neutral layer')
                        st.error('Neutral layer NOT satisfying strength', icon="🚨")
                except Exception as error:
                    st.error('Error! Something not right', icon="🚨")
                    st.write(f"An exception occurred: {type(error).__name__} {error}")
            else:
                st.write("The result will be here once clicked analysis button")
                
        with output2:
            if st.session_state.solve_clicked:
                st.header("Plot")
                st.image('images/plot_rec.png', caption='Rectangle cross-section')
            else:
                st.write("The plot result will appear here once clicked analysis button")
            
#============================= Hình tròn #=============================
    elif select == 'Circle':
        col1_1, col2_1, col3_1 = st.columns(3, gap='large')
        with col1_1:
            R = st.number_input(label="Radius (m)", min_value=0.00, step=0.01)
            thickness = st.number_input(label='Thickness (m)', min_value=0.00, step=0.01)
            st.divider()
            input_method = st.selectbox('Choose input method', ('Manual', 'From file'))
        with col2_1:
            
            if input_method == "Manual":
                max_bending_moment = st.number_input('Maximum bending moment (kNm)', step=0.01)
                max_shear_force = st.number_input('Maximum shear force (kN)', step=0.01)
                shear_force_at_maximum_moment = st.number_input('Shear force at maximum moment (kN)', step=0.01)
                # sigma = st.number_input('Allowable stress (N/m^2)', step=0.01)
                
            elif input_method == "From file":
                max_bm, max_sf, sf_at_max_bm = read_output_file()
                if max_bm != None and max_sf != None and sf_at_max_bm != None:
                    max_bending_moment = max_bm
                    max_shear_force = max_sf
                    shear_force_at_maximum_moment = sf_at_max_bm
                    st.success('Import data from file success!', icon="✅")
                    st.write(f"Maximum bending moment (kNm): {max_bm}")
                    st.write(f"Maximum shear force (kN): {max_sf}")
                    st.write(f"Shear force at maximum moment (kN): {sf_at_max_bm}")
                    # sigma = st.number_input('Allowable stress (N/m^2)', step=0.01)
                else:
                    st.error('Error! Something not right', icon="🚨")
                    
            sigma_t = st.number_input('Allowable tensile stress (N/m^2)', step=0.01)
            sigma_c = st.number_input('Allowable compress stress (N/m^2)', step=0.01)
            
        with col3_1:
            type_criterion = st.selectbox('Type criterion', ('Tresca', 'von Mises'))
            
            #==================== Button solve circle #====================
            if st.button("Clear result", type="primary"):
                st.session_state.solve_clicked = False
                
            if st.button('Analysis'):
                st.session_state.solve_clicked = True
                
                try:
                    if type_criterion == "Tresca":
                        tau = sigma_t/2
                    elif type_criterion == "von Mises":
                        tau = sigma_t/math.sqrt(3)
                        
                    Jx, Wx, sigmamin, sigmamax, taumax = hinhtron(max_bending_moment, max_shear_force, R)
                    plot_circle(R, shear_force_at_maximum_moment, sigmamin, sigmamax, taumax)
                    
                except Exception as error:
                    st.error('Error! Something not right', icon="🚨")
                    st.write(f"An exception occurred: {type(error).__name__} {error}")
                else:
                    st.success('Analysis success!', icon="✅")
                
        st.divider()
        
        output1_1, output2_1 = st.columns(2, gap='large')
        with output1_1:
            if st.session_state.solve_clicked:
                try:
                    st.header("Result:")
                    st.write("")
                    st.write(f'Moment of inertia Jx: {Jx}')
                    st.write(f'Bending moment Wx: {Wx}')
                    st.write(f'Principal stress sigma_max: {sigmamax}')
                    st.write(f'Maximun shear stress on the section: {taumax}')
                    if sigmamax <= sigma_t:
                        # st.write('Ductile (Durable) boundary layer')
                        st.success('Boundary layer satisfying strength', icon="✅")
                    else:
                        # st.write('Brittle (Not Durable) boundary layer')
                        st.error('Boundary layer NOT satisfying strength', icon="🚨")
                    if taumax <= tau:
                        # st.write('Ductile (Durable) neutral layer')
                        st.success('Neutral layer satisfying strength', icon="✅")
                    else:
                        # st.write('Brittle (Not Durable) neutral layer')
                        st.error('Neutral layer NOT satisfying strength', icon="🚨")
                except Exception as error:
                    st.error('Error! Something not right', icon="🚨")
                    st.write(f"An exception occurred: {type(error).__name__} {error}")
            else:
                st.write("The result will appear here once clicked analysis button")
                
        with output2_1:
            if st.session_state.solve_clicked:
                st.header("Plot")
                st.image('images/plot_circle.png', caption='Circle cross-section')
            else:
                st.write("The plot result will appear here once clicked analysis button")
                
#============================= Hình vành khăn #=============================
    elif select == 'Annulus':
        col1_2, col2_2, col3_2 = st.columns(3, gap='large')   
        with col1_2:
            R1 = st.number_input(label='Radius in (m)', min_value=0.00, step=0.01)  
            R2 = st.number_input(label='Radius out (m)', min_value=0.00, step=0.01)
            thickness = st.number_input(label='Thickness (m)', min_value=0.00, step=0.01)
            st.divider()
            input_method = st.selectbox('Choose input method', ('Manual', 'From file'))
        with col2_2:
            
            if input_method == "Manual":
                max_bending_moment = st.number_input('Maximum bending moment (kNm)', step=0.01)
                max_shear_force = st.number_input('Maximum shear force (kN)', step=0.01)
                shear_force_at_maximum_moment = st.number_input('Shear force at maximum moment (kN)', step=0.01)
                # sigma = st.number_input('Allowable stress (N/m^2)', step=0.01)
                
            elif input_method == "From file":
                max_bm, max_sf, sf_at_max_bm = read_output_file()
                if max_bm != None and max_sf != None and sf_at_max_bm != None:
                    max_bending_moment = max_bm
                    max_shear_force = max_sf
                    shear_force_at_maximum_moment = sf_at_max_bm
                    st.success('Import data from file success!', icon="✅")
                    st.write(f"Maximum bending moment (kNm): {max_bm}")
                    st.write(f"Maximum shear force (kN): {max_sf}")
                    st.write(f"Shear force at maximum moment (kN): {sf_at_max_bm}")
                    # sigma = st.number_input('Allowable stress (N/m^2)', step=0.01)
                else:
                    st.error('Error! Something not right', icon="🚨")
            sigma_t = st.number_input('Allowable tensile stress (N/m^2)', step=0.01)
            sigma_c = st.number_input('Allowable compress stress (N/m^2)', step=0.01)
        with col3_2:
            type_criterion = st.selectbox('Type criterion', ('Tresca', 'von Mises'))
            
            #==================== Button solve annulus #====================
            if st.button("Clear result", type="primary"):
                st.session_state.solve_clicked = False
                
            if st.button('Analysis'):
                st.session_state.solve_clicked = True
                
                try:
                    if type_criterion == "Tresca":
                        tau = sigma_t/2
                    elif type_criterion == "von Mises":
                        tau = sigma_t/math.sqrt(3)
                        
                    Jx, Wx, sigmamin, sigmamax, taumax = hinhvanhkhan(max_bending_moment, max_shear_force, R1, R2)
                    plot_annulus(R1, R2, shear_force_at_maximum_moment, sigmamin, sigmamax, taumax)
                except Exception as error:
                    st.error('Error! Something not right', icon="🚨")
                    st.write(f"An exception occurred: {type(error).__name__} {error}")
                else:
                    st.success('Analysis success!', icon="✅")
                
        st.divider()
        
        output1_2, output2_2 = st.columns(2, gap='large')
        with output1_2:
            if st.session_state.solve_clicked:
                try:
                    st.header("Result:")
                    st.write("")
                    st.write(f'Moment of inertia Jx: {Jx}')
                    st.write(f'Bending moment Wx: {Wx}')
                    st.write(f'Principal stress sigma_max: {sigmamax}')
                    st.write(f'Maximun shear stress on the section: {taumax}')
                    if sigmamax <= sigma_t:
                        # st.write('Ductile (Durable) boundary layer')
                        st.success('Boundary layer satisfying strength', icon="✅")
                    else:
                        # st.write('Brittle (Not Durable) boundary layer')
                        st.error('Boundary layer NOT satisfying strength', icon="🚨")
                    if taumax <= tau:
                        # st.write('Ductile (Durable) neutral layer')
                        st.success('Neutral layer satisfying strength', icon="✅")
                    else:
                        # st.write('Brittle (Not Durable) neutral layer')
                        st.error('Neutral layer NOT satisfying strength', icon="🚨")
                except Exception as error:
                    st.error('Error! Something not right', icon="🚨")
                    st.write(f"An exception occurred: {type(error).__name__} {error}")
            else:
                st.write("The result will appear here once clicked analysis button")
                
        with output2_2:
            if st.session_state.solve_clicked:
                st.header("Plot")
                st.image('images/plot_annulus.png', caption='Annulus cross-section')
            else:
                st.write("The plot result will appear here once clicked analysis button")
                
#============================= Hình C #=============================
    elif select == 'C shape':
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
        # st.write(type(float(selected_rows['r'])))
        st.markdown('---')
        col1_2, col2_2, col3_2 = st.columns(3, gap='large')
        with col1_2:
            thickness = st.number_input(label='Thickness (m)', min_value=0.00, step=0.01)
            st.divider()
            input_method = st.selectbox('Choose input method', ('Manual', 'From file'))
        with col2_2:
            if input_method == "Manual":
                max_bending_moment = st.number_input('Maximum bending moment (kNm)', step=0.01)
                max_shear_force = st.number_input('Maximum shear force (kN)', step=0.01)
                shear_force_at_maximum_moment = st.number_input('Shear force at maximum moment (kN)', step=0.01)
                # sigma = st.number_input('Allowable stress (N/m^2)', step=0.01)
                
            elif input_method == "From file":
                max_bm, max_sf, sf_at_max_bm = read_output_file()
                if max_bm != None and max_sf != None and sf_at_max_bm != None:
                    max_bending_moment = max_bm
                    max_shear_force = max_sf
                    shear_force_at_maximum_moment = sf_at_max_bm
                    st.success('Import data from file success!', icon="✅")
                    st.write(f"Maximum bending moment (kNm): {max_bm}")
                    st.write(f"Maximum shear force (kN): {max_sf}")
                    st.write(f"Shear force at maximum moment (kN): {sf_at_max_bm}")
                    # sigma = st.number_input('Allowable stress (N/m^2)', step=0.01)
                else:
                    st.error('Error! Something not right', icon="🚨")
            sigma_t = st.number_input('Allowable tensile stress (N/m^2)', step=0.01)
            sigma_c = st.number_input('Allowable compress stress (N/m^2)', step=0.01)
        with col3_2:
            type_criterion = st.selectbox('Type criterion', ('Tresca', 'von Mises'))
            
            #==================== Button solve C shape #====================
            if st.button("Clear result", type="primary"):
                st.session_state.solve_clicked = False
                
            if st.button('Analysis'):
                st.session_state.solve_clicked = True
                
                try:
                        
                    sigmamax, sigmatd, sigmamin, sigmamax, tau, taumax, sigmaN = hinh_I_C(type_criterion, shear_force_at_maximum_moment, max_shear_force, max_bending_moment, 
                                                        selected_rows['Sx'], selected_rows['Jx'], selected_rows['d'],
                                                        selected_rows['h'], selected_rows['t'], selected_rows['Wx'], selected_rows['Wy'],
                                                        sigma_t)
                    plot_C(shear_force_at_maximum_moment, selected_rows['h'], selected_rows['b'], selected_rows['d'], selected_rows['t'], sigmamax, sigmatd, taumax)
                    
                except Exception as error:
                    st.error('Error! Something not right', icon="🚨")
                    st.write(f"An exception occurred: {type(error).__name__} {error}")
                else:
                    st.success('Analysis success!', icon="✅")
                
        st.divider()
        
        output1_2, output2_2 = st.columns(2, gap='large')
        with output1_2:
            if st.session_state.solve_clicked:
                try:
                    st.header("Result:")
                    st.write("")
                    st.write(f'Principal stress sigma_max: {sigmamax}')
                    st.write("The cross section still has 1 dangerous layer -> calculate the special plane stress state through the intermediate layer")
                    st.write(f'Equivalent stress sigma_td: {sigmatd}')
                    st.write(f'Maximun shear stress on the section tau_max: {taumax}')
                    
                    if sigmamax <= sigma_t:
                        # st.write('Ductile (Durable) boundary layer')
                        st.success('Boundary layer satisfying strength', icon="✅")
                    else:
                        # st.write('Brittle (Not Durable) boundary layer')
                        st.error('Boundary layer NOT satisfying strength', icon="🚨")
                    if taumax <= tau:
                        # st.write('Ductile (Durable) neutral layer')
                        st.success('Neutral layer satisfying strength', icon="✅")
                    else:
                        # st.write('Brittle (Not Durable) neutral layer')
                        st.error('Neutral layer NOT satisfying strength', icon="🚨")
                        
                    st.write("Check the strength of the bar when the bar is horizontal")
                    if abs(sigmamin) > sigma_c:
                        # st.write('Ductile (Durable) horizontal bar')
                        st.success('Horizontal bar satisfying strength', icon="✅")
                    else:
                        # st.write('Brittle (Not Durable) horizontal bar')
                        st.error('Horizontal bar NOT satisfying strength', icon="🚨")
                except Exception as error:
                    st.error('Error! Something not right', icon="🚨")
                    st.write(f"An exception occurred: {type(error).__name__} {error}")
            else:
                st.write("The result will appear here once clicked analysis button")
                
        with output2_2:
            if st.session_state.solve_clicked:
                st.header("Plot")
                st.image('images/plot_C.png', caption='C shape cross-section')
            else:
                st.write("The plot result will appear here once clicked analysis button")
                
#============================= Hình I #=============================
    elif select == 'I shape':
        st.title('Cross-section I table')
        N0_values=['10', '12', '14', '16', '18', '18a', '20', '20a', '22', '22a', '24', '24a','27', '27a', '30', '30a', '33', '36', '40', '45', '50', '55', '60', '65','70', '70a', '70b']
        P_values=[111, 130, 148, 169, 187, 199, 207, 222, 237, 254, 273, 294, 315, 339, 365, 392, 422, 486, 561, 652, 761, 886, 1030, 1190, 1370, 1580, 1840]
        h_values=[100, 120, 140, 160, 180, 180, 200, 200, 220, 220, 240, 240, 270, 270, 300, 300, 330, 360, 400, 450, 500, 550, 600, 650, 700, 700, 700]
        b_values=[70, 75, 82, 90, 95, 102, 100, 110, 110, 120, 115, 125, 125, 135, 135, 145, 140, 145, 155, 160, 170, 180, 190, 200, 210, 210, 210]
        d_values=[4.5, 5, 5, 5, 5, 5, 5.2, 5.2, 5.2, 5.3, 5.6, 5.6, 6, 6, 6.5, 6.5, 7, 7.5, 8, 8.6, 9.3, 10, 10.8, 11.7, 12.7, 15, 17.]
        t_values=[7.2, 7.3, 7.5, 7.7, 8, 8.2, 8.2, 8.3, 8.6, 8.8, 9.5, 9.8, 9.8, 10.2, 10.2, 10.7, 11.2, 12.3, 13, 14.2, 15.2, 16.5, 17.8, 19.2, 20.8, 24, 28.2]
        R_values=[7, 7.5, 8, 8.5, 9, 9, 9.5, 9.5, 10, 10, 10.5, 10.5, 11, 11, 12, 12, 13, 14, 15, 16, 17, 18, 20, 22, 24, 24, 24]
        r_values=[3, 3, 3, 3.5, 3.5, 3.5, 4, 4, 4, 4, 4, 4, 4.5, 4.5, 5, 5, 5, 6, 6, 7, 7, 7, 8, 9, 10, 10, 10]
        S_values=[14.2, 16.5, 18.9, 21.5, 23.8, 25.4, 26.4, 28.3, 30.2, 32.4, 34.8, 37.5, 40.2, 43.2, 46.5, 49.9, 53.8, 61.9, 71.4, 83, 96.9, 113, 131, 151, 174, 202, 234]
        Jx_values=[244, 403, 632, 945, 1330, 1440, 1810, 1970, 2530, 2760, 3460, 3800, 5010, 5500, 7080, 7780, 9840, 13380, 18930, 27450, 39120, 54810, 75010, 100840, 133980, 152700, 175350]
        Wx_values=[48.8, 62.2, 90.3, 118, 148, 160, 181, 197, 230, 251, 289, 317, 371, 407, 472, 518, 597, 743, 947, 1220, 1560, 1990, 2500, 3100, 3830, 4360, 5010]
        ix_values=[4.15, 4.94, 5.78, 6.63, 7.47, 7.53, 8.27, 8.36, 9.14, 9.23, 9.97, 10.1, 11.2, 11.3, 12.3, 12.5, 13.5, 14.7, 16.3, 18.2, 20.1, 20.2, 23.9, 25.8, 27.7, 27.5, 27.4]
        Sx_values=[28, 38.5, 51.5, 67, 83.7, 90.1, 102, 111, 130, 141, 163, 178, 210, 229, 268, 292, 339, 423, 540, 699, 899, 1150, 1440, 1790, 2220, 2550, 2940]
        Jy_values=[35.3, 43.8, 58.2, 77.6, 94.6, 119, 112, 148, 155, 203, 198, 260, 260, 337, 337, 436, 419, 516, 666, 807, 1040, 1350, 1720, 2170, 2730, 3240, 3910]
        Wy_values=[10, 11.7, 14.2, 17.2, 19.9, 23.3, 22.4, 27, 28.2, 33.8, 34.5, 41.6, 41.5, 50, 49.9, 60.1, 59.9, 71.1, 75.9, 101, 122, 150, 181, 217, 260, 309, 373]
        iy_values=[1.58, 1.63, 1.75, 1.9, 1.99, 2.17, 2.06, 2.29, 2.26, 2.5, 2.37, 2.63, 2.54, 280, 2.69, 2.95, 2.79, 2.89, 3.05, 3.12, 3.28, 3.46, 3.62, 3.79, 3.96, 4.01, 4.09]
        
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
            'iy': ['{:.2f}'.format(val) for val in iy_values]        
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
            thickness = st.number_input(label='Thickness (m)', min_value=0.00, step=0.01)
            st.divider()
            input_method = st.selectbox('Choose input method', ('Manual', 'From file'))
        with col2_2:
            if input_method == "Manual":
                max_bending_moment = st.number_input('Maximum bending moment (kNm)', step=0.01)
                max_shear_force = st.number_input('Maximum shear force (kN)', step=0.01)
                shear_force_at_maximum_moment = st.number_input('Shear force at maximum moment (kN)', step=0.01)
                # sigma = st.number_input('Allowable stress (N/m^2)', step=0.01)
                
            elif input_method == "From file":
                max_bm, max_sf, sf_at_max_bm = read_output_file()
                if max_bm != None and max_sf != None and sf_at_max_bm != None:
                    max_bending_moment = max_bm
                    max_shear_force = max_sf
                    shear_force_at_maximum_moment = sf_at_max_bm
                    st.success('Import data from file success!', icon="✅")
                    st.write(f"Maximum bending moment (kNm): {max_bm}")
                    st.write(f"Maximum shear force (kN): {max_sf}")
                    st.write(f"Shear force at maximum moment (kN): {sf_at_max_bm}")
                    # sigma = st.number_input('Allowable stress (N/m^2)', step=0.01)
                else:
                    st.error('Error! Something not right', icon="🚨")
            sigma_t = st.number_input('Allowable tensile stress (N/m^2)', step=0.01)
            sigma_c = st.number_input('Allowable compress stress (N/m^2)', step=0.01)
        with col3_2:
            type_criterion = st.selectbox('Type criterion', ('Tresca', 'von Mises'))
            
            #==================== Button solve I shape #====================
            if st.button("Clear result", type="primary"):
                st.session_state.solve_clicked = False
                
            if st.button('Analysis'):
                st.session_state.solve_clicked = True
                
                try:
                        
                    sigmamax, sigmatd, sigmamin, sigmamax, tau, taumax, sigmaN = hinh_I_C(type_criterion, shear_force_at_maximum_moment, max_shear_force, max_bending_moment, 
                                                        selected_rows['Sx'], selected_rows['Jx'], selected_rows['d'],
                                                        selected_rows['h'], selected_rows['t'], selected_rows['Wx'], selected_rows['Wy'],
                                                        sigma_t)
                    plot_I(shear_force_at_maximum_moment, selected_rows['h'], selected_rows['b'], selected_rows['d'], selected_rows['t'], sigmamax, sigmatd, taumax)
                    
                except Exception as error:
                    st.error('Error! Something not right', icon="🚨")
                    st.write(f"An exception occurred: {type(error).__name__} {error}")
                else:
                    st.success('Analysis success!', icon="✅")
                
        st.divider()
        
        output1_2, output2_2 = st.columns(2, gap='large')
        with output1_2:
            if st.session_state.solve_clicked:
                try:
                    st.header("Result:")
                    st.write("")
                    st.write(f'Principal stress sigma_max: {sigmamax}')
                    st.write("The cross section still has 1 dangerous layer -> calculate the special plane stress state through the intermediate layer")
                    st.write(f'Equivalent stress sigma_td: {sigmatd}')
                    st.write(f'Maximun shear stress on the section tau_max: {taumax}')
                    
                    if sigmamax <= sigma_t:
                        # st.write('Ductile (Durable) boundary layer')
                        st.success('Boundary layer satisfying strength', icon="✅")
                    else:
                        # st.write('Brittle (Not Durable) boundary layer')
                        st.error('Boundary layer NOT satisfying strength', icon="🚨")
                    if taumax <= tau:
                        # st.write('Ductile (Durable) neutral layer')
                        st.success('Neutral layer satisfying strength', icon="✅")
                    else:
                        # st.write('Brittle (Not Durable) neutral layer')
                        st.error('Neutral layer NOT satisfying strength', icon="🚨")
                        
                    st.write("Check the strength of the bar when the bar is horizontal")
                    if abs(sigmamin) > sigma_c:
                        # st.write('Ductile (Durable) horizontal bar')
                        st.success('Horizontal bar satisfying strength', icon="✅")
                    else:
                        # st.write('Brittle (Not Durable) horizontal bar')
                        st.error('Horizontal bar NOT satisfying strength', icon="🚨")
                        
                except Exception as error:
                    st.error('Error! Something not right', icon="🚨")
                    st.write(f"An exception occurred: {type(error).__name__} {error}")
            else:
                st.write("The result will appear here once clicked analysis button")
                
        with output2_2:
            if st.session_state.solve_clicked:
                st.header("Plot")
                st.image('images/plot_I.png', caption='I shape cross-section')
            else:
                st.write("The plot result will appear here once clicked analysis button")

with tab3:
    st.divider()
    st.header("Nothing here")
                
