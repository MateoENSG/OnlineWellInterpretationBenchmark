import streamlit as st #1.28.0
from streamlit_drawable_canvas import st_canvas #0.9.3
from PIL import Image
import pandas as pd
import json 

# Organisation de l'app :
#   - Présentation de l'expérience
#   - Introduction du questionnaire et questionnaire -> Quelles catégories ?
#   - Introduction à l'exercice d'interpretation
#   - Affichage des données à interpreter
#   - Entrée de l'interprétation -> Quel format ?
#   - Récupération de l'interpretation ? -> Comment ?


st.set_page_config(layout="wide")  # Utilise toute la largeur de l'écran


#Presentation de l'experience

st.title("Welcome to the well log interpretation uncertainties experiment !")

st.write("The goal of this experiment is to 'quantify' the impact of an individual background and prior experiences in its interpretation of well log data.")
st.write("For that it is needed to obtain interpretation from various individuals of varying background, experiences and field.")
st.write("To participate you only need to complete the little form about 'who' you are and then to interprete the data presented to you and send the answer !")
st.write("Also, any feedback on the experiment is welcomed ! Be it on the clarity of the instructions, the GUI etc...")

#Introduction du questionnaire
st.title("Here is the form.")

#Questionnaire
status = st.text_input("Are you a student, a professional engineer or a researcher ?", "**Your status**")
field = st.radio(
    "What is your geosciences field ?",
    ["Stratigraphy", "Geology", "Geophysics", "Petrophysics", "Sedimentology", "Formation evaluation", "Geomodeling", "Statistics or geostatistics", "Machine Learning", "Applied Mathematics", "None of the above"]
)

other_field = st.text_input("If you selected 'None of the above', please specify your field :", "**Your field**")

years = st.number_input(
    "How many years of professional experience do you have in geosciences ?", value=None, placeholder="Type a number..."
)

confidence = st.radio(
    "How confident are you on well log interpretation ?",
    ["I am the best there is", "I'm excellent", "I'm quite good", "Neutral", "not particularly confident", "Not confident", "First time in my life I see well log data", "Geosciences ? What's that ?"]
)

#Enregistrement des réponses dans un fichier JSON

data = {
    "Status": status,
    "field": field,
    "other_field": other_field,
    "years": years,
    "confidence": confidence

}

if st.button("Download your answers in a JSON file !"):
    with open(r"C:\Users\e3812u\Documents\Projet_3A\OnlineWellLogInterpretation\Results\test.json", "w") as f:
        json.dump(data, f)

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
col1, col2, col3 = st.columns([1, 1, 1])
drawing_mode = col1.selectbox(
    "Drawing tool:", ("point", "freedraw", "line", "rect", "circle", "transform")
)

stroke_width = col2.slider("Stroke width: ", 1, 25, 3)
if drawing_mode == 'point':
    point_display_radius = col2.slider("Point display radius: ", 1, 25, 3)
stroke_color = col1.color_picker("Stroke color hex: ")
#bg_color = col3.color_picker("Background color hex: ", "#eee")
bg_image =  r"Data\test_well_log.png" #Forced background = well log.

realtime_update = col3.checkbox("Update in realtime", True)

    

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
    point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
    key="canvas",
)





