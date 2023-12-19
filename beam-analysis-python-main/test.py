import streamlit as st

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

# Example usage
max_bm, max_sf, sf_at_max_bm = read_output_file()
print(f"Max Bending Moment: {max_bm}")
print(f"Max Shear Force: {max_sf}")
print(f"Shear Force at Max Bending Moment: {sf_at_max_bm}")