# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


st.set_page_config(
    page_title="Cơ học vật rắn biến dạng",
    layout='wide',
    initial_sidebar_state='auto'
)
st.title('Cơ học vật rắn biến dạng')
data = {
    'Tên': ['Lê Thành', 'Huỳnh Thạch Thảo', 'Hoàng Quốc Thái', 'Võ Trung Hiếu', 'Vũ Hoàng Khả Vy'],
    'MSSV': ['2153800', '2153805','2153788','','2153994']
}
df = pd.DataFrame(data)
st.table(df)