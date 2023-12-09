from typing import Any
import numpy as np
import streamlit as st
from streamlit.hello.utils import show_code
from streamlit_option_menu import option_menu 
from indeterminatebeam import *
import pandas as pd

# Kiểm tra nếu 'console_forces' không tồn tại trong session state thì khởi tạo
if 'console_forces' not in st.session_state:
    st.session_state.console_forces = []

# Kiểm tra nếu 'beam_forces' không tồn tại trong session state thì khởi tạo
if 'beam_forces' not in st.session_state:
    st.session_state.beam_forces = []

if 'advanced_forces' not in st.session_state:
    st.session_state.advanced_forces = []

if 'type_support' not in st.session_state:
    st.session_state.type_support = []

# Biến trạng thái để kiểm soát việc hiển thị và tính toán
if 'solve_clicked' not in st.session_state:
    st.session_state.solve_clicked = False

console_bm_max, console_sf_max, console_max_bm_pos, console_sf_at_bm_max = None, None, None, None
beam2sp_bm_max, beam2sp_sf_max, beam2sp_max_bm_pos, beam2sp_sf_at_bm_max = None, None, None, None
advanced_bm_max, advanced_sf_max, advanced_max_bm_pos, advanced_sf_at_bm_max = None, None, None, None

def calculate_shear_force_and_bending_moment(length):
    # Tính shear force và bending moment tại từng vị trí
    positions = [i * 0.5 for i in range(int(2 * length))]
    shear_forces = [beam.get_shear_force(pos) for pos in positions]
    bending_moments = [beam.get_bending_moment(pos) for pos in positions]

    # Tìm vị trí của bending moment max
    max_bending_moment_position = positions[bending_moments.index(max(map(abs, bending_moments)))]

    # Tính shear force tại vị trí bending moment max
    shear_force_at_max_bending_moment = beam.get_shear_force(max_bending_moment_position)

    return max_bending_moment_position, shear_force_at_max_bending_moment


st.set_page_config(page_title="Beam Calculator", page_icon="🙃", layout="wide")
st.markdown("# Beam Calculator")
st.sidebar.header("Beam Calculator Tool")
st.markdown("---")

# Tạo các tab
tab1, tab2, tab3 = st.tabs(["Theory", "Input", "Output"])
# Tab về lý thuyết
with tab1:
    # Hiển thị lý thuyết với đường link đến tài liệu
    st.title('Theory')
    st.markdown('''<p style="font-size:20px; text-align:justyfy">A brief overview of the engineering theory and conventions used in this program are illustrated below. Theory is adapted from the Hibbeler textbook [2]. A more rigorous overview of the basic theory behind statically determinate structures is presented in the beambending package documentation.</p>''',unsafe_allow_html=True)
    st.link_button('Click here!','https://indeterminatebeam.readthedocs.io/en/main/theory.html?fbclid=IwAR18lJpYVJm1MnqkVdXydhA0eLWQwSmCV4w6VzKAIK5dueK9zq-_gYrxMy0')
    st.markdown('---')
    st.title('Sign convention')
    st.markdown('''<p style="font-size:20px; text-align:justyfy">For External Forces the following convention is used:</p>''',unsafe_allow_html=True)
    st.markdown('''<p style="font-size:20px; text-align:justyfy">+ For x direction: To the right is positive</p>''',unsafe_allow_html=True)
    st.markdown('''<p style="font-size:20px; text-align:justyfy">+ For y direction: Up is positive</p>''',unsafe_allow_html=True)
    st.markdown('''<p style="font-size:20px; text-align:justyfy">+ For m direction: Anti-clockwise is positive</p>''',unsafe_allow_html=True)
    st.image('images/signconvention.jpg')
    st.markdown('''<p style="font-size:20px; text-align:justyfy">For internal forces considering the left of a cut:</p>''',unsafe_allow_html=True)
    st.markdown('''<p style="font-size:20px; text-align:justyfy">+ For axial force (x direction): To the right is positive</p>''',unsafe_allow_html=True)
    st.markdown('''<p style="font-size:20px; text-align:justyfy">+ For shear force (y direction): Down is positive</p>''',unsafe_allow_html=True)
    st.markdown('''<p style="font-size:20px; text-align:justyfy">+ For moments: Anti-clockwise is positive</p>''',unsafe_allow_html=True)
    st.image('images/internalforces.jpg')
    st.markdown('''<p style="font-size:20px; text-align:justyfy">For deflections:</p>''',unsafe_allow_html=True)
    st.markdown('''<p style="font-size:20px; text-align:justyfy">+ Up is considered positive</p>''',unsafe_allow_html=True)
    st.markdown('''<p style="font-size:20px; text-align:justyfy">For angled point loads (assuming a positive force is used):</p>''',unsafe_allow_html=True)
    st.markdown('''<p style="font-size:20px; text-align:justyfy">+ An angle of 0 indicates a positive force to the right</p>''',unsafe_allow_html=True)
    st.markdown('''<p style="font-size:20px; text-align:justyfy">+ An angle between 0 and 90 indicates a positive force to the right and a positive force up</p>''',unsafe_allow_html=True)
    st.markdown('''<p style="font-size:20px; text-align:justyfy">+ An angle of 90 indicates a positive force up</p>''',unsafe_allow_html=True)
    st.markdown('''<p style="font-size:20px; text-align:justyfy">+ An angle between 90 and 180 degrees indicates a force acting left (negative direction) and a positive force acting up</p>''',unsafe_allow_html=True)
    st.markdown('''<p style="font-size:20px; text-align:justyfy">+ An angle of 180 indicates a negative horizontal force</p>''',unsafe_allow_html=True)
    st.image('images/angle.jpg')
    st.link_button('Click here!','https://indeterminatebeam.readthedocs.io/en/main/theory.html?fbclid=IwAR0PBvCzt8FYlYfQ8vIDRMNVBxjC1y0FVLY63nYmZFvk9gwCpKBIS5pT9oI#sign-convention')
    
# Tab nhập liệu
added_forces=[]
added_support=[]

with tab2:
    # Tab nhập liệu
    select = st.selectbox('Beam type', ('Console', 'Beam with 2 supports','Complex beam'))
    st.markdown('---')
    
    #================================= Chọn Console #=================================
    if select == 'Console':
        col1, col2, col3 = st.columns(3)
        # Tạo hộp để nhập số liệu
        with col1: 
            length = st.number_input(label='Length (m)', min_value=1.00, max_value=None, step=0.01)
            st.markdown('---')
            
            fixed_type = st.selectbox('Fixed position', ('Fixed left end', 'Fixed right end'))
            
        with col2:
            type_load = st.selectbox('Type forces', ('Point load', 'Distributed load', 'Moment')) 
            if type_load == 'Point load':
                magnitude = st.number_input('Magnitude (kN)', step=0.01)
                position = st.slider('Position (m)', min_value=0.00, max_value=length, step=0.1)
                angle = st.number_input('Angle (degree)', max_value=360.00, value=90.00 ,step=0.01)
                if st.button('Add'):
                    st.session_state.console_forces.append({'Type Load': type_load, 'Magnitude': magnitude, 'Position': position, 'Angle': angle})
            elif type_load == 'Moment':
                magnitude = st.number_input('Magnitude (kN)', step=0.01)
                position = st.slider('Position (m)', min_value=0.00, max_value=length, step=0.1)
                if st.button('Add'):
                    st.session_state.console_forces.append({'Type Load': type_load, 'Magnitude': magnitude, 'Position': position})
            
            elif type_load == 'Distributed load':
                # Vừa tạo hộp nhập số liệu, vừa tạo slider
                magnitude = st.number_input('Magnitude (kN)', step=0.01)
                start_point = st.slider('Start position (m)', min_value=0.00, max_value=length, step=0.1)
                end_point = st.slider('End position (m)', min_value=0.00, max_value=length, step=0.1)
                if st.button('Add'):
                    st.session_state.console_forces.append({'Type Load': type_load, 'Magnitude': magnitude, 'Start Position': start_point, 'End Position': end_point})

        # Hiển thị các lực đã thêm vào (Console)
        with col3: 
            st.write('Added forces:')
            for idx, force in enumerate(st.session_state.console_forces, start=1):
                delete_checkbox = st.checkbox(f"Delete load {idx}")
                st.write(f"{idx}. Type load is {force['Type Load']}, Magnitude: {force['Magnitude']} (kN)" +
                    (f", Position: {force['Position']} (m)" if force['Type Load'] in ['Point load', 'Moment'] else "") +
                    (f", Angle: {force['Angle']} (degree)" if 'Angle' in force else "") +  # Add this line for displaying the angle
                    (f", Start Position: {force['Start Position']} (m)" if 'Start Position' in force else "") +
                    (f", End Position: {force['End Position']} (m)" if 'End Position' in force else ""))
                if delete_checkbox:
                    st.session_state.console_forces.pop(idx - 1)
                    
            #================================= Check button #=================================         
            #Button để tạo beam, add sp và lực, hiển thị đề bài        
            if st.button('Check'):
                
                try:
                    #Tạo beam với độ dài length
                    beam = Beam(length)
                    
                    if fixed_type == "Fixed left end":
                        beam.add_supports(Support(0, (1,1,1)))
                    else: beam.add_supports(Support(length, (1,1,1)))
                    
                    for force in st.session_state.console_forces:
                        # Trích xuất thông tin từ mỗi phần tử
                        type_load = force.get("Type Load")
                        magnitude = force.get("Magnitude")
                        angle = force.get("Angle")
                        position = force.get("Position", None)
                        start_position = force.get("Start Position", None)
                        end_position = force.get("End Position", None)

                        # Gọi hàm add_load với thông tin từng load
                        if type_load == "Distributed load":
                            beam.add_loads(DistributedLoadV(round(magnitude,2), (float(start_position), float(end_position))))
                        elif type_load == "Moment":
                            beam.add_loads(PointTorque(round(magnitude,2), position))
                        elif type_load == "Point load" and angle == 90:
                            beam.add_loads(PointLoadV(round(magnitude,2), position))
                        elif type_load == "Point load" and angle != 90:
                            beam.add_loads(PointLoad(round(magnitude,2), position, angle=angle))

                    beam.analyse()
                    #Vẽ biểu đồ dựa trên thông tin đã input
                    fig_beam = beam.plot_beam_diagram()
                    fig_beam.write_image("./images/fig_beam_console.png",format='png',engine='kaleido')
                except:
                    st.error('Error! Something not right', icon="🚨")
                else:
                    st.success('Plotting success!', icon="✅")
      
        st.markdown('---')
        keo, bua, bao = st.columns([1,3,1])
        with bua:
          st.image('images/fig_beam_console.png', caption='Console beam', width=700)
          
        #================================= Solve button #================================= 
        st.markdown('---')
        if st.button('Solve'):
            st.session_state.solve_clicked = True
            
            try: 
                #Tạo beam với độ dài length
                beam = Beam(length)
                
                if fixed_type == "Fixed left end":
                    beam.add_supports(Support(0, (1,1,1)))
                else: beam.add_supports(Support(length, (1,1,1)))
                
                for force in st.session_state.console_forces:
                    # Trích xuất thông tin từ mỗi phần tử
                    type_load = force.get("Type Load")
                    magnitude = force.get("Magnitude")
                    angle = force.get("Angle")
                    position = force.get("Position", None)
                    start_position = force.get("Start Position", None)
                    end_position = force.get("End Position", None)

                    # Gọi hàm add_load với thông tin từng load
                    if type_load == "Distributed load":
                        beam.add_loads(DistributedLoadV(round(magnitude,2), (float(start_position), float(end_position))))
                    elif type_load == "Moment":
                        beam.add_loads(PointTorque(round(magnitude,2), position))
                    elif type_load == "Point load" and angle==90:
                        beam.add_loads(PointLoadV(round(magnitude,2), position))
                    elif type_load == "Point load" and angle != 90:
                        beam.add_loads(PointLoad(round(magnitude,2), position, angle=angle))
                        
                beam.analyse()
                #Giải và plot đồ thị
                #PLot beam schematic
                fig_reac = beam.plot_reaction_force()
                fig_reac.write_image("./images/fig_reac_console.png",format='png',engine='kaleido')

                #PLot normal force
                fig_normal = beam.plot_normal_force()
                fig_normal.write_image("./images/fig_normal_console.png",format='png',engine='kaleido')

                #PLot shear force
                fig_shear = beam.plot_shear_force()
                fig_shear.write_image("./images/fig_shear_console.png",format='png',engine='kaleido')

                #PLot bending moment
                fig_moment = beam.plot_bending_moment()
                fig_moment.write_image("./images/fig_moment_console.png",format='png',engine='kaleido')

                #Plot deflection
                fig_deflection = beam.plot_deflection()
                fig_deflection.write_image("./images/fig_deflection_console.png",format='png',engine='kaleido')
                
                console_bm_max = beam.get_bending_moment(return_absmax = True)
                console_sf_max = beam.get_shear_force(return_absmax = True)
                console_max_bm_pos, console_sf_at_bm_max = calculate_shear_force_and_bending_moment(length)
                
            except:
                st.error('Error! Something not right', icon="🚨")
            else:
                st.success('Calculation success!', icon="✅")
                
    #================================= Beam with 2 supports #=================================
    elif select == 'Beam with 2 supports':
        col1_1, col1_2, col1_3, col1_4 = st.columns(4, gap='large')
        
        with col1_1:
            length_1 = st.number_input(label='Length (m)', min_value=1.00, max_value=None, step=0.01)
            st.markdown('---')
            support_type_left = st.selectbox('Support type left', ('Pin', 'Roller'))
            support_type_right = st.selectbox('Support type right', ('Pin', 'Roller'))
            
        
        with col1_2:
            sup_1 = st.slider("Position of support 1 (m)", 0.00, length_1, None, step=0.1)
            sup_2 = st.slider("Position of support 2 (m)", 0.00, length_1, None, step=0.1)
            
        with col1_3:
            type_load_1 = st.selectbox('Type forces', ('Point load', 'Distributed load', 'Moment'))
            st.markdown('---')
            if type_load_1 == 'Point load':
                magnitude_1 = st.number_input('Magnitude (kN)', step=0.01)
                position_1 = st.slider('Position (m)', min_value=0.00, max_value=length_1, step=0.1)
                angle_1 =st.number_input('Angle (degree)', max_value=360.00, value=90.00 , step=0.01)
                if st.button('Add'):
                    st.session_state.beam_forces.append({'Type Load': type_load_1, 'Magnitude': magnitude_1, 'Position': position_1, 'Angle': angle_1})
            
            elif type_load_1 == 'Moment':
                magnitude_1 = st.number_input('Magnitude (kN)', step=0.01)
                position_1 = st.slider('Position (m)', min_value=0.00, max_value=length_1, step=0.1)
                if st.button('Add'):
                    st.session_state.beam_forces.append({'Type Load': type_load_1, 'Magnitude': magnitude_1, 'Position': position_1})
            
            elif type_load_1 == 'Distributed load':
                magnitude_1 = st.number_input('Magnitude (kN)', step=0.01)
                start_point_1 = st.slider('Start position (m)', min_value=0.00, max_value=length_1, step=0.1)
                end_point_1 = st.slider('End position (m)', min_value=0.00, max_value=length_1, step=0.1)
                if st.button('Add'):
                    st.session_state.beam_forces.append({'Type Load': type_load_1, 'Magnitude': magnitude_1, 'Start Position': start_point_1, 'End Position': end_point_1})
            
        with col1_4:
            st.write('Added forces:')
            for idx, force in enumerate(st.session_state.beam_forces, start=1):
                delete_checkbox_1 = st.checkbox(f"Delete load {idx}")
                st.write(f"{idx}. Type load is {force['Type Load']}, Magnitude: {force['Magnitude']} (kN)" + 
                        (f", Position: {force['Position']} (m)" if force['Type Load'] in ['Point load', 'Moment'] else "") +
                        (f", Angle: {force['Angle']} (degree)" if 'Angle' in force else "") + 
                        (f", Start Position: {force['Start Position']} (m)" if 'Start Position' in force else "") +
                        (f", End Position: {force['End Position']} (m)" if 'End Position' in force else ""))
                if delete_checkbox_1:
                    st.session_state.beam_forces.pop(idx - 1)
                    
            #================================= Check button #=================================         
            if st.button('Check'):
                
                try:
                    #Tạo beam với độ dài length
                    beam = Beam(length_1)
                    
                    if support_type_left == "Pin":
                        beam.add_supports(Support(sup_1, (1,1,0)))
                    elif support_type_left == "Roller": 
                        beam.add_supports(Support(sup_1, (0,1,0)))
                        
                    if support_type_right == "Pin":
                        beam.add_supports(Support(sup_2, (1,1,0)))
                    elif support_type_right == "Roller":
                        beam.add_supports(Support(sup_2, (0,1,0)))
                        
                    for force in st.session_state.beam_forces:
                        # Trích xuất thông tin từ mỗi phần tử
                        type_load = force.get("Type Load")
                        magnitude = force.get("Magnitude")
                        angle = force.get("Angle")
                        position = force.get("Position", None)
                        start_position = force.get("Start Position", None)
                        end_position = force.get("End Position", None)

                        # Gọi hàm add_load với thông tin từng load
                        if type_load == "Distributed load":
                            beam.add_loads(DistributedLoadV(round(magnitude,2), (float(start_position), float(end_position))))
                        elif type_load == "Moment":
                            beam.add_loads(PointTorque(round(magnitude,2), position))
                        elif type_load == "Point load" and angle==90:
                            beam.add_loads(PointLoadV(round(magnitude,2), position))
                        elif type_load == "Point load" and angle != 90:
                            beam.add_loads(PointLoad(round(magnitude,2), position, angle=angle))

                    #Vẽ biểu đồ dựa trên thông tin đã input
                    fig_beam = beam.plot_beam_diagram()
                    fig_beam.write_image("./images/fig_beam_2sp.png",format='png',engine='kaleido')
                except:
                    st.error('Error! Something not right', icon="🚨")
                else:
                    st.success('Plotting success!', icon="✅")
        
        st.markdown('---')        
        keo1, bua1, bao1 = st.columns([1,3,1])
        with bua1:
          st.image('images/fig_beam_2sp.png', caption='Beam with 2 supports', width=700)             
        st.markdown('---')
        
        #================================= Solve button #================================= 
        if st.button('Solve'):
            st.session_state.solve_clicked = True
            
            try:
                #Tạo beam với độ dài length
                beam = Beam(length_1)
                
                if support_type_left == "Pin":
                    beam.add_supports(Support(sup_1, (1,1,0)))
                elif support_type_left == "Roller": 
                    beam.add_supports(Support(sup_1, (0,1,0)))
                    
                if support_type_right == "Pin":
                    beam.add_supports(Support(sup_2, (1,1,0)))
                elif support_type_right == "Roller":
                    beam.add_supports(Support(sup_2, (0,1,0)))
                
                for force in st.session_state.beam_forces:
                    # Trích xuất thông tin từ mỗi phần tử
                    type_load = force.get("Type Load")
                    magnitude = force.get("Magnitude")
                    angle = force.get("Angle")
                    position = force.get("Position", None)
                    start_position = force.get("Start Position", None)
                    end_position = force.get("End Position", None)

                    # Gọi hàm add_load với thông tin từng load
                    if type_load == "Distributed load":
                        beam.add_loads(DistributedLoadV(round(magnitude,2), (float(start_position), float(end_position))))
                    elif type_load == "Moment":
                        beam.add_loads(PointTorque(round(magnitude,2), position))
                    elif type_load == "Point load" and angle==90:
                        beam.add_loads(PointLoadV(round(magnitude,2), position))
                    elif type_load == "Point load" and angle != 90:
                        beam.add_loads(PointLoad(round(magnitude,2), position, angle=angle))
                        
                beam.analyse()
                #Giải và plot đồ thị
                #PLot beam schematic
                fig_reac = beam.plot_reaction_force()
                fig_reac.write_image("./images/fig_reac_2sp.png",format='png',engine='kaleido')

                #PLot normal force
                fig_normal = beam.plot_normal_force()
                fig_normal.write_image("./images/fig_normal_2sp.png",format='png',engine='kaleido')

                #PLot shear force
                fig_shear = beam.plot_shear_force()
                fig_shear.write_image("./images/fig_shear_2sp.png",format='png',engine='kaleido')

                #PLot bending moment
                fig_moment = beam.plot_bending_moment()
                fig_moment.write_image("./images/fig_moment_2sp.png",format='png',engine='kaleido')

                #Plot deflection
                fig_deflection = beam.plot_deflection()
                fig_deflection.write_image("./images/fig_deflection_2sp.png",format='png',engine='kaleido')

                beam2sp_bm_max = beam.get_bending_moment(return_absmax = True)
                beam2sp_sf_max = beam.get_shear_force(return_absmax = True)
                beam2sp_max_bm_pos, beam2sp_sf_at_bm_max = calculate_shear_force_and_bending_moment(length_1)

            except:
                st.error('Error! Something not right', icon="🚨")
            else:
                st.success('Calculation success!', icon="✅")

    #================================= Complex beam #=================================       
    elif select == 'Complex beam':
        col2_1, col2_2, col2_3, col2_4 = st.columns(4, gap='large')
        
        with col2_1:
            length_2 = st.number_input(label='Length (m)', min_value=1.00, max_value=None, step=0.01)
            st.markdown('---')
            type_support = st.selectbox('Type support', ('Fixed', 'Roller', 'Pin'))
            st.markdown('---')
            
            if type_support == 'Roller':
                roller = st.slider('Roller position (m)', min_value=0.00, max_value=length_2, step=0.1)
                if st.button('Add type support'):
                    st.session_state.type_support.append({'Type support': type_support, 'Position': roller})
            
            elif type_support == 'Pin':
                pin = st.slider('Pin position (m)', min_value=0.00, max_value=length_2, step=0.1)
                if st.button('Add type support'):
                    st.session_state.type_support.append({'Type support': type_support, 'Position': pin})
            
            elif type_support == 'Fixed':
                fixed_left_end = st.checkbox('Fixed left end')
                fixed_right_end = st.checkbox('Fixed right end')
                if st.button('Add type support'):
                    support_info = {'Type support': type_support}
                    if fixed_left_end:
                        support_info['Fixed left end'] = True
                    if fixed_right_end:
                        support_info['Fixed right end'] = True
                    st.session_state.type_support.append(support_info)
                    
        with col2_2:
            st.write('Added support:')
            for idx, support in enumerate(st.session_state.type_support, start=1):
                delete_checkbox = st.checkbox(f"Delete {support['Type support']} {idx}")
                support_text = f"{idx}. Type support is {support['Type support']}"
                if 'Position' in support:
                    support_text += f", Position: {support['Position']} (m)"
                if 'Fixed left end' in support:
                    support_text += ", Fixed left end"
                if 'Fixed right end' in support:
                    support_text += ", Fixed right end"
                st.write(support_text)        
                if delete_checkbox:
                    st.session_state.type_support.pop(idx - 1)
        
        with col2_3:
            type_load_2 = st.selectbox('Type forces', ('Point load', 'Distributed load', 'Moment'))
            st.markdown('---')
            if type_load_2 == 'Point load':
                magnitude_2 = st.number_input('Magnitude (kN)', step=0.01)
                position_2 = st.slider('Position (m)', min_value=0.00, max_value=length_2, step=0.1)
                angle_2 = st.number_input('Angle (degree)', max_value=360.00, value=90.00 , step=0.1)
                if st.button('Add'):
                    st.session_state.advanced_forces.append({'Type Load': type_load_2, 'Magnitude': magnitude_2, 'Position': position_2, 'Angle': angle_2})
            elif type_load_2 == 'Moment':
                magnitude_2 = st.number_input('Magnitude (kN)', step=0.01)
                position_2 = st.slider('Position (m)', min_value=0.00, max_value=length_2, step=0.1)
                if st.button('Add'):
                    st.session_state.advanced_forces.append({'Type Load': type_load_2, 'Magnitude': magnitude_2, 'Position': position_2})
            elif type_load_2 == 'Distributed load':
                magnitude_2 = st.number_input('Magnitude (kN)', step=0.01)
                start_point_2 = st.slider('Start position (m)', min_value=0.00, max_value=length_2, step=0.1)
                end_point_2 = st.slider('End position (m)', min_value=0.00, max_value=length_2, step=0.1)
                if st.button('Add'):
                    st.session_state.advanced_forces.append({'Type Load': type_load_2, 'Magnitude': magnitude_2, 'Start Position': start_point_2, 'End Position': end_point_2})
            
        with col2_4:
            st.write('Added forces:')
            for idx, force in enumerate(st.session_state.advanced_forces, start=1):
                delete_checkbox_2= st.checkbox(f"Delete load {idx}")
                st.write(f"{idx}. Type load is {force['Type Load']}, Magnitude: {force['Magnitude']} (kN)" +
                        (f", Position: {force['Position']} (m)" if force['Type Load'] in ['Point load', 'Moment'] else "") +
                        (f", Angle: {force['Angle']} (degree)" if 'Angle' in force else "") +  
                        (f", Start Position: {force['Start Position']} (m)" if 'Start Position' in force else "") +
                        (f", End Position: {force['End Position']} (m)" if 'End Position' in force else ""))
                if delete_checkbox_2:
                    st.session_state.advanced_forces.pop(idx - 1) 
                    
            #================================= Check button #=================================         
            if st.button('Check'):
                st.session_state.quick_solve_clicked = True

                try:
                    #Tạo beam với độ dài length
                    beam = Beam(length_2)
                    
                    # st.write(st.session_state.type_support)
                    
                    for support in st.session_state.type_support:
                        # Trích xuất thông tin từ mỗi phần tử
                        type_support = support.get("Type support")
                        position = support.get("Position", None)

                        # Gọi hàm add_load với thông tin từng load
                        if type_support == "Pin":
                            beam.add_supports(Support(position, (1,1,0)))
                        elif type_support == "Roller":
                            beam.add_supports(Support(position, (0,1,0)))
                        elif type_support == "Fixed":
                            if 'Fixed left end' in support:
                                beam.add_supports(Support(0, (1,1,1)))
                            if 'Fixed right end' in support:
                                beam.add_supports(Support(length_2, (1,1,1)))
                        
                    for force in st.session_state.advanced_forces:
                        # Trích xuất thông tin từ mỗi phần tử
                        type_load = force.get("Type Load")
                        magnitude = force.get("Magnitude")
                        angle = force.get("Angle")
                        position = force.get("Position", None)
                        start_position = force.get("Start Position", None)
                        end_position = force.get("End Position", None)

                        # Gọi hàm add_load với thông tin từng load
                        if type_load == "Distributed load":
                            beam.add_loads(DistributedLoadV(round(magnitude,2), (float(start_position), float(end_position))))
                        elif type_load == "Moment":
                            beam.add_loads(PointTorque(round(magnitude,2), position))
                        elif type_load == "Point load" and angle==90:
                            beam.add_loads(PointLoadV(round(magnitude,2), position))
                        elif type_load == "Point load" and angle != 90:
                            beam.add_loads(PointLoad(round(magnitude,2), position, angle=angle))

                    #Vẽ biểu đồ dựa trên thông tin đã input
                    fig_beam = beam.plot_beam_diagram()
                    fig_beam.write_image("./images/fig_beam_advanced.png",format='png',engine='kaleido')
                    
                except:
                    st.error('Error! Something not right', icon="🚨")
                else:
                    st.success('Plotting success!', icon="✅")
            
        st.markdown('---')
        
        keo2, bua2, bao2 = st.columns([1,3,1])
        with bua2:
          st.image('images/fig_beam_advanced.png', caption='Beam with many supports', width=700)       
        st.markdown('---')
        
        #================================= Solve button #================================= 
        if st.button('Solve'):
            st.session_state.solve_clicked = True
            
            try:
                #Tạo beam với độ dài length
                beam = Beam(length_2)
                
                # st.write(st.session_state.type_support)
                
                for support in st.session_state.type_support:
                    # Trích xuất thông tin từ mỗi phần tử
                    type_support = support.get("Type support")
                    position = support.get("Position", None)

                    # Gọi hàm add_load với thông tin từng load
                    if type_support == "Pin":
                        beam.add_supports(Support(position, (1,1,0)))
                    elif type_support == "Roller":
                        beam.add_supports(Support(position, (0,1,0)))
                    elif type_support == "Fixed":
                        if 'Fixed left end' in support:
                            beam.add_supports(Support(0, (1,1,1)))
                        if 'Fixed right end' in support:
                            beam.add_supports(Support(length_2, (1,1,1)))
                    
                for force in st.session_state.advanced_forces:
                    # Trích xuất thông tin từ mỗi phần tử
                    type_load = force.get("Type Load")
                    magnitude = force.get("Magnitude")
                    angle = force.get("Angle")
                    position = force.get("Position", None)
                    start_position = force.get("Start Position", None)
                    end_position = force.get("End Position", None)

                    # Gọi hàm add_load với thông tin từng load
                    if type_load == "Distributed load":
                        beam.add_loads(DistributedLoadV(round(magnitude,2), (float(start_position), float(end_position))))
                    elif type_load == "Moment":
                        beam.add_loads(PointTorque(round(magnitude,2), position))
                    elif type_load == "Point load" and angle == 90:
                        beam.add_loads(PointLoadV(round(magnitude,2), position))
                    elif type_load == "Point load" and angle != 90:
                        beam.add_loads(PointLoad(round(magnitude,2), position, angle=angle))

                #Vẽ biểu đồ dựa trên thông tin đã input
                beam.analyse()
                #Giải và plot đồ thị
                #PLot beam schematic
                fig_reac = beam.plot_reaction_force()
                fig_reac.write_image("./images/fig_reac_advanced.png",format='png',engine='kaleido')

                #PLot normal force
                fig_normal = beam.plot_normal_force()
                fig_normal.write_image("./images/fig_normal_advanced.png",format='png',engine='kaleido')

                #PLot shear force
                fig_shear = beam.plot_shear_force()
                fig_shear.write_image("./images/fig_shear_advanced.png",format='png',engine='kaleido')

                #PLot bending moment
                fig_moment = beam.plot_bending_moment()
                fig_moment.write_image("./images/fig_moment_advanced.png",format='png',engine='kaleido')

                #Plot deflection
                fig_deflection = beam.plot_deflection()
                fig_deflection.write_image("./images/fig_deflection_advanced.png",format='png',engine='kaleido')

                advanced_bm_max = beam.get_bending_moment(return_absmax = True)
                advanced_sf_max = beam.get_shear_force(return_absmax = True)
                advanced_max_bm_pos, advanced_sf_at_bm_max = calculate_shear_force_and_bending_moment(length_2)

            except:
                st.error('Error! Something not right', icon="🚨")
            else:
                st.success('Calculation success!', icon="✅")
                
#================================= Output tab #=================================         
with tab3:
    image = st.selectbox('Problem', ('Console', 'Beam with 2 supports', 'Complex beam'))
    if image == 'Console':
        keo3, bua3, bao3 = st.columns([1,3,1])
        with bua3:
            st.write("")
            st.divider()
            st.write(f"Bending moment absolute max: {console_bm_max}")
            st.write(f"Shear force absolute max: {console_sf_max}")
            st.write(f"Shear force at position of absolute max bending moment ({console_max_bm_pos} m): {console_sf_at_bm_max}")
            
            st.divider()
            st.image('images/fig_reac_console.png', caption='Reaction force diagram', width=700)
            st.divider()

            st.image('images/fig_shear_console.png', caption='Shear force diagram', width=700)
            st.divider()

            st.image('images/fig_normal_console.png', caption='Normal force diagram', width=700)
            st.divider()

            st.image('images/fig_moment_console.png', caption='Bending moment diagram', width=700)
    
    elif image == 'Beam with 2 supports': 
        keo3, bua3, bao3 = st.columns([1,3,1])
        with bua3:
            st.write("")
            st.divider()
            st.write(f"Bending moment absolute max: {beam2sp_bm_max}")
            st.write(f"Shear force absolute max: {beam2sp_sf_max}")
            st.write(f"Shear force at position of absolute max bending moment ({beam2sp_max_bm_pos} m): {beam2sp_sf_at_bm_max}")
            
            st.divider()
            st.image('images/fig_reac_2sp.png', caption='Reaction force diagram', width=700)
            st.divider()

            st.image('images/fig_shear_2sp.png', caption='Shear force diagram', width=700)
            st.divider()

            st.image('images/fig_normal_2sp.png', caption='Normal force diagram', width=700)
            st.divider()

            st.image('images/fig_moment_2sp.png', caption='Bending moment diagram', width=700)
    
    elif image == 'Complex beam':
        keo3, bua3, bao3 = st.columns([1,3,1])
        with bua3:
            st.write("")
            st.divider()
            st.write(f"Bending moment absolute max: {advanced_bm_max}")
            st.write(f"Shear force absolute max: {advanced_sf_max}")
            st.write(f"Shear force at position of absolute max bending moment ({advanced_max_bm_pos} m): {advanced_sf_at_bm_max}")
            
            st.divider()
            st.image('images/fig_reac_advanced.png', caption='Reaction force diagram', width=700)
            st.divider()

            st.image('images/fig_shear_advanced.png', caption='Shear force diagram', width=700)
            st.divider()

            st.image('images/fig_normal_advanced.png', caption='Normal force diagram', width=700)
            st.divider()

            st.image('images/fig_moment_advanced.png', caption='Bending moment diagram', width=700)
    

    

