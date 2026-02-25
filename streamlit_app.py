import streamlit as st
import numpy as np
from PIL import Image
import easyocr

st.set_page_config(page_title="Scanner Pro", layout="wide")

st.markdown("""
    <style>
    .container { position: relative; display: inline-block; }
    .overlay-btn {
        position: absolute;
        transform: translate(-50%, -50%);
        z-index: 10;
        cursor: pointer;
        width: 30px;
        height: 30px;
        accent-color: #00ff00;
    }
    .item-label {
        position: absolute;
        background: rgba(255, 255, 255, 0.8);
        padding: 2px 5px;
        border-radius: 3px;
        font-size: 12px;
        pointer-events: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📸 Scanner Interactivo")
st.write("Marcá los ítems directamente sobre tu foto.")

archivo = st.file_uploader("Subí la foto de tu lista", type=["jpg", "png", "jpeg"])

if archivo:
    img = Image.open(archivo)
    ancho_orig, alto_orig = img.size
    
    # Mostramos la imagen ocupando el ancho disponible
    ancho_display = 800 
    escala = ancho_display / ancho_orig
    alto_display = alto_orig * escala

    if 'resultados' not in st.session_state:
        with st.spinner('Escaneando posiciones...'):
            reader = easyocr.Reader(['es'])
            st.session_state['resultados'] = reader.readtext(np.array(img))

    # Contenedor para la imagen y los botones
    html_botones = ""
    for i, (bbox, texto, prob) in enumerate(st.session_state['resultados']):
        # Calculamos el centro del texto detectado
        centro_x = (bbox[0][0] + bbox[2][0]) / 2 * escala
        centro_y = (bbox[0][1] + bbox[2][1]) / 2 * escala
        
        # Creamos un checkbox HTML para cada posición
        html_botones += f'''
            <input type="checkbox" class="overlay-btn" 
                   style="left: {centro_x}px; top: {centro_y}px;">
        '''

    # Renderizamos la imagen con los botones encima
    st.markdown(
        f'''
        <div class="container" style="width: {ancho_display}px; height: {alto_display}px;">
            <img src="data:image/jpeg;base64,{st.image(img, output_format="JPEG", width=ancho_display)}" 
                 style="width: 100%; position: absolute; top: 0; left: 0;">
            {html_botones}
        </div>
        ''', 
        unsafe_allow_html=True
    )
