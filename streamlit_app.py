import streamlit as st
import numpy as np
from PIL import Image
import easyocr

st.set_page_config(page_title="Lista Inteligente", page_icon="👍")

# Estilo para los botones de Like y el tachado
st.markdown("""
    <style>
    .stCheckbox { background-color: #f0f2f6; padding: 20px; border-radius: 15px; margin-bottom: 10px; border-left: 8px solid #007bff; }
    .stMarkdown del { color: #888; text-decoration: line-through; }
    </style>
    """, unsafe_allow_html=True)

st.title("📸 Scanner de Listas")

archivo = st.file_uploader("Saca una foto a tu lista", type=["jpg", "png", "jpeg"])

if archivo:
    img = Image.open(archivo)
    if st.button("🔍 IDENTIFICAR LISTA"):
        with st.spinner('La IA está leyendo tu letra...'):
            reader = easyocr.Reader(['es'])
            st.session_state['items'] = reader.readtext(np.array(img), detail=0)

    if 'items' in st.session_state:
        st.write("---")
        for i, texto in enumerate(st.session_state['items']):
            col1, col2 = st.columns([0.2, 0.8])
            with col1:
                # El botón de Like para tachar
                listo = st.checkbox("👍", key=f"item_{i}")
            with col2:
                if listo:
                    st.markdown(f"~~{texto}~~ ✅")
                else:
                    st.markdown(f"**{texto}**")
