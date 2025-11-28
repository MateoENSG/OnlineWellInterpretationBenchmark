import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import json

st.title("Canvas avec téléchargement")

# Options de dessin
drawing_mode = st.sidebar.selectbox(
    "Mode de dessin:",
    ("freedraw", "line", "rect", "circle", "transform")
)

stroke_width = st.sidebar.slider("Épaisseur du trait:", 1, 25, 3)

# Canvas
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color="#000000",
    background_color="#ffffff",
    height=400,
    width=600,
    drawing_mode=drawing_mode,
    key="canvas",
)

# Section de téléchargement
st.subheader("Télécharger votre dessin")

col1, col2 = st.columns(2)

with col1:
    if canvas_result.image_data is not None:
        img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        
        st.download_button(
            label="📥 Télécharger l'image (PNG)",
            data=buf.getvalue(),
            file_name="mon_dessin.png",
            mime="image/png"
        )

with col2:
    if canvas_result.json_data is not None:
        json_string = json.dumps(canvas_result.json_data, indent=2)
        
        st.download_button(
            label="📥 Télécharger les données (JSON)",
            data=json_string,
            file_name="donnees_canvas.json",
            mime="application/json"
        )

# Afficher les informations
if canvas_result.json_data is not None:
    objects = canvas_result.json_data.get("objects", [])
    if objects:
        st.info(f"✏️ {len(objects)} objet(s) dessiné(s)")
        
        

# Points clés
# canvas_result.image_data : contient l'image complète du canvas sous forme de tableau numpy (RGBA)
# canvas_result.json_data : contient les données vectorielles des objets dessinés (coordonnées, styles, etc.)
# Le format JSON est utile si vous voulez recharger le dessin plus tard ou faire des manipulations sur les formes
# Le format PNG/image est parfait pour une utilisation directe de l'image

# Les deux formats sont complémentaires selon vos besoins !