import streamlit as st #1.50.0
from streamlit_drawable_canvas import st_canvas #0.9.3
from PIL import Image
import pandas as pd
import json 
import lasio 
import lasio.examples
import matplotlib.pyplot as plt
import numpy as np
import uuid


def main():

    st.set_page_config(layout="wide")

    st.logo("Data/ringlogo.png", size="large")

    #Presentation de l'experience

    st.title("Welcome to the well log interpretation uncertainties experiment !")

    st.write("The goal of this experiment is to 'quantify' the impact of an individual background and prior experiences in its interpretation of well log data.")
    st.write("For that it is needed to obtain interpretation from various individuals of varying background, experiences and field.")
    st.write("To participate you only need to complete the little form about 'who' you are and then to interprete the data presented to you and send the answer !")
    st.write("Also, any feedback on the experiment is welcomed ! Be it on the clarity of the instructions, the GUI etc...")


    tab1, tab2 = st.tabs(["Form", "Interpretation"])

    with tab1:
        status = st.radio("Are you a student, a professional engineer or a researcher ?", 
                        ["Student", "Engineer", "Researcher", st.text_input("Other : ", 
                                                                            " Your status")]
        )

        field = st.radio(
            "What is your geosciences field ?",
            ["Stratigraphy", "Geology", "Geophysics", "Petrophysics", "Sedimentology", 
             "Formation evaluation", "Geomodeling", "Statistics or geostatistics", 
             "Machine Learning", "Applied Mathematics", st.text_input("Other : ", "Your field")]
        )

        sector = st.radio("What is your sector of activity ?", 
                             ["geothermal", "oil and gas", "mineral ressources", "hydrogeology", "geosciences software",
                             "geotechnics", "Polluted soil/ Environmental remediatio"]
        )

        years = st.number_input(
            "How many years of professional experience do you have in geosciences ?", 
            value=None, placeholder="Type a number..."
        )

        confidence = st.radio(
            "How confident are you on well log interpretation ?",
            ["I am the best there is", "I'm excellent", "I'm quite good", "Neutral", 
             "not particularly confident", "Not confident", 
             "First time in my life I see well log data", "Geosciences ? What's that ?"]
        )



    with tab2:
        col1, col2 = st.columns(2)

        with col1:
            drawing_mode = col1.selectbox(
                "Drawing tool:", ("point", "freedraw", "line", "rect", "circle", "transform")
            )

            stroke_width = st.slider("Stroke width: ", 1, 25, 3)
            if drawing_mode == 'point':
                point_display_radius = st.slider("Point display radius: ", 1, 25, 3)
            stroke_color = st.color_picker("Stroke color hex: ")
            bg_image =  r"Data\test_well_log.png" #Forced background = well log.

            realtime_update = st.checkbox("Update in realtime", True)


        with col2:
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




if __name__ == "__main__":
    main()
