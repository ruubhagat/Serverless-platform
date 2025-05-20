# Warmup.py
import streamlit as st
from utils import list_functions, warmup_function

st.title("🔥 Warmup Function Container")

functions = list_functions()
function_options = {f"{func['id']}: {func['name']}": func["id"] for func in functions}

selected_function = st.selectbox("Select Function", list(function_options.keys()))
runtime = st.selectbox("Select Runtime", ["runc", "runsc"])

if st.button("Warmup"):
    func_id = function_options[selected_function]
    response = warmup_function(func_id, runtime)
    if response.status_code == 200:
        st.success("Container warmed up successfully!")
        st.json(response.json())
    else:
        st.error("Failed to warm up container.")
