import streamlit as st
import numpy as np
from PIL import Image
import easyocr

st.set_page_config(page_title="Mi Lista", layout="centered")

# Truco de diseño para que el texto y el Like estén en la misma línea
st.markdown("""
    <style>
    [data-testid="column"] {
        display: flex;
        align-items: center;
    }
    .stCheckbox { margin-bottom: 0 !important; }
    .item-texto { font-size: 20px; font-weight: bold; margin-left: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📸 Scanner de Lista")

archivo = st.file_uploader("Foto de la lista", type=["jpg", "png", "jpeg"])

if archivo:
    img = Image.open(archivo)
    st.image(img, use_container_width=True)
    
    if st.button("🔍 IDENTIFICAR"):
        with st.spinner('Escaneando...'):
            reader = easyocr.Reader(['es'])
            st.session_state['mi_lista'] = reader.readtext(np.array(img), detail=0)

    if 'mi_lista' in st.session_state:
        st.write("---")
        for i, texto in enumerate(st.session_state['mi_lista']):
            # Definimos dos columnas muy pegaditas
            c1, c2 = st.columns([0.15, 0.85])
            
            with c1:
                # El pulgar para marcar
                marcado = st.checkbox("", key=f"ch_{i}")
            
            with c2:
                # El nombre al lado
                if marcado:
                    st.markdown(f"~~{texto}~~ ✅")
                else:
                    st.markdown(f"**{texto}**")
