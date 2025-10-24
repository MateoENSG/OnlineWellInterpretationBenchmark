import streamlit as st #1.50.0
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw
import io
import pandas as pd
import json 
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
        col1, col2 = st.columns([0.15, 0.85])
        
        # Initialize session state for storing lines
        if 'lines' not in st.session_state:
            st.session_state.lines = []
        
        # PREDEFINED LINE TYPES - Customize these as needed
        LINE_TYPES = {
            "Major Regression": {
                "style": "Solid",
                "color": "#FF0000",  # Red
                "thickness": 2
            },
            "Major Transgression": {
                "style": "Solid",
                "color": "#0000FF",  # Blue
                "thickness": 2
            },
            "Minor regression": {
                "style": "Solid",
                "color": "#00FF00",  # Green
                "thickness": 1
            },
            "Minor transgression": {
                "style": "Solid",
                "color": "#FFA500",  # Orange
                "thickness": 1
            }
        }
        
        with col1:
            st.write("**Interpretation Tools**")
            
            # Line type selector - user only chooses from predefined types
            selected_line = st.selectbox(
                "Select line type:",
                options=list(LINE_TYPES.keys()),
                key="line_type_selector"
            )
            
            # Display the properties of the selected line type - To comment in final product
            st.write("**Line Properties:**")
            line_props = LINE_TYPES[selected_line]
            st.write(f"- Style: {line_props['style']}")
            st.write(f"- Color: {line_props['color']}")
            st.write(f"- Thickness: {line_props['thickness']}px")
            
            # Clear all lines button
            if st.button("Clear All Lines"):
                st.session_state.lines = []
                st.rerun()
            
            # Display current lines info - To comment in final product
            if st.session_state.lines:
                st.write(f"**Lines drawn:** {len(st.session_state.lines)}")
                st.write("**Line types used:**")
                for i, line in enumerate(st.session_state.lines, 1):
                    st.write(f"{i}. {line['name']} at y={line['y']}")
        
        with col2:
            # Load the base image
            from PIL import Image, ImageDraw
            import tempfile
            import os
            
            base_image = Image.open(r"Data/test_well_log.png")
            
            # Convert to RGB if necessary to ensure color
            if base_image.mode != 'RGB':
                base_image = base_image.convert('RGB')
            
            # Create a copy to draw on
            image_with_lines = base_image.copy()
            draw = ImageDraw.Draw(image_with_lines)
            
            # Draw all stored lines
            for line in st.session_state.lines:
                y = line['y']
                color = line['color']
                thickness = line['thickness']
                style = line['style']
                
                # Convert hex color to RGB
                color_rgb = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                
                # Draw based on line style
                if style == "Solid":
                    draw.line([(0, y), (base_image.width, y)], fill=color_rgb, width=thickness)
                elif style == "Dashed":
                    dash_length = 20
                    gap_length = 10
                    x = 0
                    while x < base_image.width:
                        draw.line([(x, y), (min(x + dash_length, base_image.width), y)], 
                                fill=color_rgb, width=thickness)
                        x += dash_length + gap_length
                elif style == "Dotted":
                    dot_spacing = 10
                    for x in range(0, base_image.width, dot_spacing):
                        draw.ellipse([(x - thickness//2, y - thickness//2), 
                                    (x + thickness//2, y + thickness//2)], 
                                    fill=color_rgb)
                elif style == "Dash-Dot":
                    dash_length = 20
                    dot_gap = 5
                    gap_length = 10
                    x = 0
                    while x < base_image.width:
                        # Dash
                        draw.line([(x, y), (min(x + dash_length, base_image.width), y)], 
                                fill=color_rgb, width=thickness)
                        x += dash_length + dot_gap
                        # Dot
                        if x < base_image.width:
                            draw.ellipse([(x - thickness//2, y - thickness//2), 
                                        (x + thickness//2, y + thickness//2)], 
                                        fill=color_rgb)
                        x += dot_gap + gap_length
            
            # Save to temporary file - use fixed name to keep coordinates consistent
            temp_dir = tempfile.gettempdir()
            temp_filename = "well_log_annotated.png"
            temp_path = os.path.join(temp_dir, temp_filename)
            image_with_lines.save(temp_path, format='PNG')
            
            # Display image with fixed key to maintain coordinate system
            coord = streamlit_image_coordinates(
                temp_path, 
                use_column_width="always",
                key="image_coord_main"
            )
            # st.title(f"coord y {coord['y']}") #TypeError: 'NoneType' object is not subscriptable
            # st.title(f"coord y {coord.get('y')}") #AttributeError: 'NoneType' object has no attribute 'get'
            
            # When user clicks, add a new line
            if coord is not None and coord.get('y') is not None:
                line_props = LINE_TYPES[selected_line]
                new_line = {
                    'name': selected_line,
                    'y': coord['y'],
                    'color': line_props['color'],
                    'thickness': line_props['thickness'],
                    'style': line_props['style']
                }
                
                # Check if line at this exact position already exists
                line_exists = any(line['y'] == coord['y'] for line in st.session_state.lines)
                
                if not line_exists:
                    st.session_state.lines.append(new_line)
                    st.rerun()
            
            st.write(f"**Click coordinates:** {coord}")


if __name__ == "__main__":
    main()
