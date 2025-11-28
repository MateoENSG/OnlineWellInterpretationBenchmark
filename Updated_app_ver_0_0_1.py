import streamlit as st #1.28.0
from streamlit_drawable_canvas import st_canvas #0.9.3
from PIL import Image
import io
import pandas as pd
import json 
import uuid

# Organisation de l'app :
#   - Présentation de l'expérience
#   - Introduction du questionnaire et questionnaire -> Quelles catégories ?
#   - Introduction à l'exercice d'interpretation
#   - Affichage des données à interpreter
#   - Entrée de l'interprétation -> Quel format ?
#   - Récupération de l'interpretation ? -> Comment ?


st.set_page_config(layout="wide")  # Utilise toute la largeur de l'écran

# Générer un ID de session unique (persistant pendant toute la session)
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

session_id = st.session_state.session_id

st.write(f"ID de session : {session_id}")

#Presentation de l'experience

st.title("Welcome to the well log interpretation uncertainties experiment !")

st.write("The goal of this experiment is to 'quantify' the impact of an individual background and prior experiences in its interpretation of well log data.")
st.write("For that it is needed to obtain interpretation from various individuals of varying background, experiences and field.")
st.write("To participate you only need to complete the little form about 'who' you are and then to interprete the data presented to you and send the answer !")
st.write("Also, any feedback on the experiment is welcomed ! Be it on the clarity of the instructions, the GUI etc...")


#Introduction du questionnaire
st.title("Here is the form.")

#Questionnaire
status = st.multiselect("Are you a student, an engineer and/or a researcher ?", ["Student", "Engineer", "Researcher"])
field = st.multiselect(
    "What is your geosciences field ?",
    ["Stratigraphy", "Geology", "Geophysics", "Petrophysics", "Sedimentology", "Formation evaluation", "Geomodeling", "Statistics or geostatistics", "Machine Learning", "Applied Mathematics", "None of the above"]
)

other_field = st.text_input("If you selected 'None of the above', please specify your field :")

years = st.number_input(
    "How many years of professional experience do you have in geosciences ?", value=None, placeholder="Type a number..."
)

confidence = st.radio(
    "How confident are you on well log interpretation ?",
    ["I am the best there is", "I'm excellent", "I'm quite good", "Neutral", "not particularly confident", "Not confident", "First time in my life I see well log data", "Geosciences ? What's that ?"]
)

mail = st.text_input("If you wish to receive updates on the experiment and your results, could you write an email contact down ?")

#Enregistrement des réponses dans un fichier JSON

data = {
    "Status": status,
    "field": field,
    "other_field": other_field,
    "years": years,
    "confidence": confidence,
    "mail": mail

}

# Vérifier si au moins une question a une réponse
if status or field or years is not None or confidence or (mail and mail != "**Your email contact**"):
    json_string = json.dumps(data, indent=2, ensure_ascii=False)
    
    st.download_button(
        label="📥 Télécharger vos réponses (JSON)",
        data=json_string,
        file_name=f"form_{session_id}.json",
        mime="application/json"
    )
else:
    st.info("Veuillez répondre à au moins une question pour télécharger vos réponses.")



#Introduction à l'expérience d'interpretation
st.title("The interpretation experiment")
st.write("Now that you have filled the form you can go ahead and interprete the data presented in the next section.")
st.write("The objective is for you to make annotations, to write ideas and basically any form of interpretation of the data you can think of.")

#Présentation des données a interpreter
st.title("Data presentation")
st.write("The data you are to interprete is/is from a public dataset available on INSERT DATA ORIGIN")

#Interpretation
st.title("Interpretation")

# Specify canvas parameters in application
col1, col2 = st.columns([1, 1])

drawing_mode = col1.selectbox(
    "Drawing tool:", ("line", "transform")
)

line_type = col2.selectbox(
    "Type of line:", ("Major Transgression", "Minor Transgression", "Major Regression", "Minor Regression")
)

# stroke_width = col2.slider("Stroke width: ", 1, 25, 3)
# stroke_color = col1.color_picker("Stroke color hex: ")

if line_type == "Major Transgression" :
    stroke_width = 6
    stroke_color = "rgba(0, 0, 255, 1)"

if line_type == "Minor Transgression" :
    stroke_width = 3
    stroke_color = "rgba(0, 0, 255, 1)"

if line_type == "Major Regression" :
    stroke_width = 6
    stroke_color = "rgba(255, 0, 0, 1)"

if line_type == "Minor Regression" :
    stroke_width = 3
    stroke_color = "rgba(255, 0, 0, 1)"

bg_image =  r"Data\test_well_log.png" #Forced background = well log.

realtime_update = True 

# Create a canvas component
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    #background_color=bg_color,
    background_image=Image.open(bg_image) if bg_image else None,
    update_streamlit=realtime_update,
    height=750,
    width=800,
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
            file_name=f"canvas_{session_id}.png",
            mime="image/png"
        )

with col2:
    if canvas_result.json_data is not None:
        json_string = json.dumps(canvas_result.json_data, indent=2)
        
        st.download_button(
            label="📥 Télécharger les données (JSON)",
            data=json_string,
            file_name=f"donnees_canvas_{session_id}.json",
            mime="application/json"
        )

# Afficher les informations
if canvas_result.json_data is not None:
    objects = canvas_result.json_data.get("objects", [])
    if objects:
        st.info(f"✏️ {len(objects)} objet(s) dessiné(s)")
