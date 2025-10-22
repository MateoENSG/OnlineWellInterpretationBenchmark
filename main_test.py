import streamlit as st #1.50.0
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image
import pandas as pd
import json 
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
        col1, col2 = st.columns([0.3,0.7])

        with col1:
            

        with col2:
            coord = streamlit_image_coordinates(r"Data/test_well_log.png", use_column_width="always")
            st.write(coord)

            #With what is just up I can get the coordinates of a clic and so I can use them to add lines !!!





if __name__ == "__main__":
    main()
