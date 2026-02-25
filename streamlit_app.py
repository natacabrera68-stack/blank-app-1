import streamlit as st
import numpy as np
from PIL import Image
import easyocr

st.set_page_config(page_title="Mi Lista", page_icon="👍")

# Estilo para que los renglones sean claros y el botón esté pegado al texto
st.markdown("""
    <style>
    .stCheckbox { 
        margin-bottom: 0px;
        padding: 5px;
    }
    .item-text {
        font-size: 18px;
        font-weight: bold;
        padding-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📸 Scanner de Compras")

archivo = st.file_uploader("Subí o sacá foto a la lista", type=["jpg", "png", "jpeg"])

if archivo:
    img = Image.open(archivo)
    # Foto arriba para referencia rápida
    st.image(img, use_container_width=True)
    
    if st.button("🔍 IDENTIFICAR ITEMS"):
        with st.spinner('Escaneando...'):
            reader = easyocr.Reader(['es'])
            # Filtramos textos cortos o vacíos para que la lista quede limpia
            resultados = reader.readtext(np.array(img), detail=0)
            st.session_state['lista'] = [res for res in resultados if len(res) > 1]

    if 'lista' in st.session_state:
        st.write("---")
        for i, item in enumerate(st.session_state['lista']):
            # Creamos dos columnas: una para el Like y otra para el Nombre
            col1, col2 = st.columns([0.2, 0.8])
            
            with col1:
                tacho = st.checkbox("👍", key=f"check_{i}")
            
            with col2:
                if tacho:
                    st.markdown(f"<div class='item-text'><del>{item}</del> ✅</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='item-text'>{item}</div>", unsafe_allow_html=True)
        
        if st.button("Limpiar todo"):
            del st.session_state['lista']
            st.rerun()
