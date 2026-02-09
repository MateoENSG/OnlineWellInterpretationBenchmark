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

# Generation of a unique session ID (persistant troughout the entire session)
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

session_id = st.session_state.session_id

st.write(f"ID de session : {session_id}")

#Presentation 

st.title("Welcome to the well log interpretation uncertainties experiment !")

#using columns in order to put a space on the left of the text. Aesthetic thing.

col1, col2 = st.columns([0.015, 0.985])
with col2:
    st.write("The goal of this experiment is to 'quantify' the impact of an individual background and prior experiences in its interpretation of well log data.")
    st.write("For that it is needed to obtain interpretation from various individuals of varying background, experiences and field.")
    st.write("To participate you only need to complete the little form about 'who' you are and then to interprete the data presented to you and send the answer !")
    st.write("Also, any feedback on the experiment is welcomed ! Be it on the clarity of the instructions, the GUI etc...")


#Form introduction
st.title("Here is the form.")

with st.expander("Form"):
    #Form
    status = st.multiselect("Are you a student, an engineer and/or a researcher ?", ["Student", "Engineer", "Researcher"])
    field = st.multiselect(
        "What is your geosciences field ?",
        ["Stratigraphy", "Geology", "Geophysics", "Petrophysics", "Sedimentology", "Formation evaluation", "Geomodeling", "Statistics or geostatistics", "Machine Learning", "Applied Mathematics", "None of the above"]
    )

    other_field = st.text_input("If you selected 'None of the above', please specify your field :")

    years = st.number_input(
        "How many years of professional experience do you have in geosciences ?", value=None, placeholder="Type a number..."
    )

    confidence = st.selectbox(
        "How confident are you on well log interpretation ?",
        ["I am the best there is", "I'm excellent", "I'm quite good", "Neutral", "not particularly confident", "Not confident", "First time in my life I see well log data", "Geosciences ? What's that ?"],
        index=None,
        placeholder="Select your confidence level"
    )

    mail = st.text_input("If you wish to receive updates on the experiment and your results, could you write an email contact down ?")

    #Saving the answers in a JSON file
    data = {
        "Status": status,
        "field": field,
        "other_field": other_field,
        "years": years,
        "confidence": confidence,
        "mail": mail

    }

    # Check if at least one question was answered to allow the download
    if status or field or years is not None or confidence or (mail and mail != "**Your email contact**"):
        json_string = json.dumps(data, indent=2, ensure_ascii=False)
        
        st.download_button(
            label="📥 Download your answers (JSON)",
            data=json_string,
            file_name=f"form_{session_id}.json",
            mime="application/json"
        )
    else:
        st.info("Please answer at least one question in order to download your form.")



#Introduction to the interpretation
st.title("The interpretation experiment")

col1, col2 = st.columns([0.015, 0.985])
with col2:
    st.write("Now that you have filled the form you can go ahead and interprete the data presented in the next section.")
    st.write("The objective is for you to make annotations, to write ideas and basically any form of interpretation of the data you can think of.")

#Data introduction
st.title("Data presentation")
col1, col2 = st.columns([0.015, 0.985])
with col2:
    st.write("The data you are to interprete is/is from a public dataset available on INSERT DATA ORIGIN")

#Interpretation
st.title("Interpretation")
st.write("Here you can use the various drawing tools to interpret de log. You also have an area where you can enter text to details your interpretation.")
st.write("Note that you might have to wait a second or two when modifying the drawing tool or the type of line you are using to ensure the modification is effective.")

# Specify canvas parameters in application
col1, col2 = st.columns([1, 1])

#Drawing_mode
drawing_mode = col1.selectbox(
    "Drawing tool:", ("line", "transform", "rect", "freedraw")
)

if drawing_mode == "line":
    line_type = col2.selectbox(
        "Type of line:", ("Major Transgression", "Minor Transgression", "Major Regression", "Minor Regression")
    )

if drawing_mode == "rect":
    line_type = col2.selectbox(
        "Type of line:", ("Oil", "Water", "Major Regression", "Minor Regression")
    )    

if drawing_mode == "transform":
    line_type = "Transform"

if drawing_mode == "freedraw":
    line_type = "Freedraw"

#Line_type

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

if line_type == "Oil" :
    stroke_width = 3
    stroke_color = "rgba(255, 0, 0, 1)"

if line_type == "Water" :
    stroke_width = 3
    stroke_color = "rgba(0, 0, 255, 1)"

if line_type == "Transform" :
    stroke_width = 1
    stroke_color = "rgba(255, 0, 0, 1)"

if line_type == "Freedraw" :
    stroke_width = col2.slider("Stroke width: ", 1, 25, 3)
    stroke_color = col1.color_picker("Stroke color hex: ")

bg_image =  r"C:\Users\e3812u\Documents\Projet_3A\OnlineWellLogInterpretation\Data\logs_from_OceanDrillingProgram\182-1128D_logs_selected_and_cropped_2.png" #Forced background = well log.

realtime_update = True 

# Create a canvas component
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    #background_color=bg_color,
    background_image=Image.open(bg_image) if bg_image else None,
    update_streamlit=realtime_update,
    height=1050,
    width=1100,
    drawing_mode=drawing_mode,
    key="canvas",
)

interpretation = st.text_area("Write your interpretation here")
data = {
    "Interpretation" : interpretation
    }

# Check if interpretation isn't empty
if interpretation is not None:
    json_string = json.dumps(data, indent=2, ensure_ascii=False)
    
    st.download_button(
        label="📥 Download your interpretation",
        data=json_string,
        file_name=f"interpretation_{session_id}.json",
        mime="application/json"
    )
else:
    st.info("Please enter an interpretation to allow the download.")

# Section de téléchargement
st.subheader("Download your drawing")

col1, col2 = st.columns(2)

with col1:
    if canvas_result.image_data is not None:
        img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        
        st.download_button(
            label="📥 Download the image (PNG)",
            data=buf.getvalue(),
            file_name=f"canvas_{session_id}.png",
            mime="image/png"
        )

with col2:
    if canvas_result.json_data is not None:
        json_string = json.dumps(canvas_result.json_data, indent=2)
        
        st.download_button(
            label="📥 Download the image's data (JSON)",
            data=json_string,
            file_name=f"data_canvas_{session_id}.json",
            mime="application/json"
        )

# Afficher les informations
if canvas_result.json_data is not None:
    objects = canvas_result.json_data.get("objects", [])
    if objects:
        st.info(f"✏️ {len(objects)} objet(s) dessiné(s)")


