import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        .main {
            background-color: #f7f9fc;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        </style>
    """, unsafe_allow_html=True)
