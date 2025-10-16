import streamlit as st #1.50.0
from PIL import Image
import pandas as pd
import json 
import lasio 
import lasio.examples
import matplotlib.pyplot as plt
import numpy as np
import uuid


def main():


    # Organisation de l'app :
    #   - Présentation de l'expérience
    #   - Introduction du questionnaire et questionnaire -> Quelles catégories ?
    #   - Introduction à l'exercice d'interpretation
    #   - Affichage des données à interpreter
    #   - Entrée de l'interprétation -> Quel format ?
    #   - Récupération de l'interpretation ? -> Comment ?


    st.set_page_config(layout="wide")  # Utilise toute la largeur de l'écran

    #UUID
    my_uuid = uuid.uuid4()


    #Presentation de l'experience

    st.title("Welcome to the well log interpretation uncertainties experiment !")

    st.write("The goal of this experiment is to 'quantify' the impact of an individual background and prior experiences in its interpretation of well log data.")
    st.write("For that it is needed to obtain interpretation from various individuals of varying background, experiences and field.")
    st.write("To participate you only need to complete the little form about 'who' you are and then to interprete the data presented to you and send the answer !")
    st.write("Also, any feedback on the experiment is welcomed ! Be it on the clarity of the instructions, the GUI etc...")

    #Introduction du questionnaire
    st.title("Here is the form.")

    #Questionnaire
    status = st.radio("Are you a student, a professional engineer or a researcher ?", 
                      ["Student", "Engineer", "Researcher", "Autre"])
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

    ##Enregistrement des réponses dans un fichier JSON

    # data = {
    #     "uuid": my_uuid,
    #     "Status": status,
    #     "field": field,
    #     "other_field": other_field,
    #     "years": years,
    #     "confidence": confidence

    # }

    # # Bouton de téléchargement JSON
    # json_str = json.dumps(data, indent=2)
    # st.download_button(
    #     label="💾 Télécharger JSON",
    #     data=json_str,
    #     file_name="lignes_graph.json",
    #     mime="application/json"
    # )

    #Introduction à l'expérience d'interpretation
    st.title("The interpretation experiment")
    st.write("Now that you have filled the form you can go ahead and interprete the data presented in the next section.")
    st.write("The objective is for you to make annotations, to write ideas and basically any form of interpretation of the data you can think of.")

    #Présentation des données a interpreter
    st.title("Data presentation")
    st.write("The data you are to interprete is/is from a public dataset available on INSERT DATA ORIGIN")



    #Interpretation
    st.title("Interpretation")


    #Chargement des donnees

    # Initialiser l'état de session
    if 'h_lines' not in st.session_state:
        st.session_state.h_lines = []
    if 'v_lines' not in st.session_state:
        st.session_state.v_lines = []

    # Charger le fichier LAS
    las = lasio.examples.open("1001178549.las")
    df = las.df()

    # Afficher le dataframe
    with st.expander("📊 Voir les données brutes"):
        st.dataframe(df)

    # Configuration
    col_config1, col_config2 = st.columns(2)
    with col_config1:
        logs_per_row = st.slider("Logs per row", min_value=3, max_value=8, value=5)
    with col_config2:
        fig_height = st.slider("Figure height", min_value=6, max_value=15, value=10)

    # Sidebar pour les options des lignes
    st.sidebar.header("⚙️ Options des lignes")

    line_color_h = st.sidebar.color_picker("Couleur lignes horizontales", "#FF0000")
    line_color_v = st.sidebar.color_picker("Couleur lignes verticales", "#00FF00")
    line_width = st.sidebar.slider("Épaisseur des lignes", 0.5, 3.0, 1.5)

    # Bouton pour effacer toutes les lignes
    if st.sidebar.button("🗑️ Effacer toutes les lignes", use_container_width=True):
        st.session_state.h_lines = []
        st.session_state.v_lines = []
        st.rerun()

    # Obtenir les limites de depth
    depth_min, depth_max = float(df.index.min()), float(df.index.max())

    # Define log groups
    log_groups = {
        'Gamma Ray': ['GR', 'CGR', 'SGR', 'HSGR', 'THOR', 'URAN', 'POTA'],
        'Resistivity': ['ILD', 'ILM', 'ILS', 'SFLU', 'LLD', 'LLS', 'MSFL', 'RES', 'RT', 'RILD', 'RILM'],
        'Porosity': ['NPHI', 'DPHI', 'RHOB', 'DT', 'PHIT', 'PHIE', 'DTS', 'DTSM'],
        'Sonic': ['DT', 'DTC', 'DTS', 'DTCO', 'DTSM', 'AC', 'SONIC'],
        'Density': ['RHOB', 'RHOZ', 'ZDEN', 'DRHO', 'DEN'],
        'Neutron': ['NPHI', 'TNPH', 'NPOR', 'NEU'],
        'Caliper': ['CALI', 'CAL', 'HCAL', 'C1', 'C2'],
        'SP': ['SP', 'SPT'],
        'Other': []
    }

    # Categorize columns into groups
    categorized = {group: [] for group in log_groups.keys()}
    used_columns = set()
    for column in df.columns:
        column_upper = column.upper()
        assigned = False
    
        for group_name, keywords in log_groups.items():
            if group_name == 'Other':
                continue
            for keyword in keywords:
                if keyword in column_upper:
                    categorized[group_name].append(column)
                    used_columns.add(column)
                    assigned = True
                    break
            if assigned:
                break
    
        if not assigned:
            categorized['Other'].append(column)

    # Afficher les informations
    st.write(f"**Total logs available: {len(df.columns)}**")
    st.write(f"**Depth range: {depth_min:.2f} - {depth_max:.2f}**")

    # Sidebar pour ajouter des lignes de référence
    st.sidebar.markdown("---")
    st.sidebar.header("➕ Ajouter des lignes de référence")

    tab_h, tab_v = st.sidebar.tabs(["🔴 Horizontales", "🟢 Verticales"])

    with tab_h:
        st.markdown("#### Ligne horizontale (Depth)")
        slider_depth = st.slider(
            "Position (Depth)",
            min_value=depth_min,
            max_value=depth_max,
            value=float(np.mean([depth_min, depth_max])),
            step=1.0,
            key="slider_depth"
        )
        st.info(f"📍 Valeur: **Depth = {slider_depth:.2f}**")
        
        if st.button("➕ Ajouter cette ligne", use_container_width=True, key="add_h"):
            if not any(abs(slider_depth - existing) < 0.1 for existing in st.session_state.h_lines):
                st.session_state.h_lines.append(round(slider_depth, 2))
                st.success(f"✅ Ligne ajoutée: Depth={slider_depth:.2f}")
                st.rerun()
            else:
                st.warning("⚠️ Cette ligne existe déjà")

    with tab_v:
        st.markdown("#### Ligne verticale (Valeur log)")
        # Les lignes verticales seront dynamiques selon le log affiché
        st.info("Les lignes verticales s'ajoutent directement sur les graphiques")

    # Display each group
    for group_name, group_columns in categorized.items():
        if not group_columns:
            continue
    
        st.write(f"## {group_name} Logs ({len(group_columns)} logs)")
        st.write(f"Logs: {', '.join(group_columns)}")
    
        # Calculate rows needed for this group
        n_logs = len(group_columns)
        n_rows = int(np.ceil(n_logs / logs_per_row))
    
        # Create plots for each row in this group
        for row in range(n_rows):
            start_idx = row * logs_per_row
            end_idx = min(start_idx + logs_per_row, n_logs)
            row_columns = group_columns[start_idx:end_idx]
        
            # Créer un expander pour chaque rangée de logs
            with st.expander(f"📈 {group_name} - Row {row + 1}", expanded=True):
                # Container pour les lignes verticales
                col_add_v, col_manage_v = st.columns([1, 1])
                
                with col_add_v:
                    st.markdown("**➕ Ajouter une ligne verticale**")
                    new_v_line = st.number_input(
                        "Valeur log:",
                        value=0.0,
                        step=1.0,
                        key=f"new_v_{group_name}_{row}"
                    )
                    if st.button("Ajouter", key=f"add_v_{group_name}_{row}"):
                        if not any(abs(new_v_line - existing) < 0.01 for existing in st.session_state.v_lines):
                            st.session_state.v_lines.append(round(new_v_line, 2))
                            st.success(f"✅ Ligne verticale ajoutée: {new_v_line:.2f}")
                            st.rerun()
                
                with col_manage_v:
                    if st.session_state.v_lines:
                        st.markdown(f"**📋 Lignes verticales ({len(st.session_state.v_lines)})**")
                        for i, val in enumerate(sorted(st.session_state.v_lines)):
                            col1, col2 = st.columns([3, 1])
                            col1.markdown(f"x = {val:.2f}")
                            if col2.button("❌", key=f"del_v_{val}_{group_name}_{row}_{i}"):
                                st.session_state.v_lines.remove(val)
                                st.rerun()
        
                # Create figure for this row
                fig, axes = plt.subplots(1, len(row_columns), figsize=(15, fig_height), sharey=True)
            
                # Handle case where there's only one subplot
                if len(row_columns) == 1:
                    axes = [axes]
            
                for i, column in enumerate(row_columns):
                    # Récupérer les min/max du log pour les lignes verticales
                    col_min = df[column].min()
                    col_max = df[column].max()
                    
                    axes[i].plot(df[column], df.index, linewidth=0.8, color='steelblue')
                    axes[i].set_xlabel(column, fontsize=10, fontweight='bold')
                    axes[i].invert_yaxis()  # Depth increases downward
                    axes[i].grid(True, alpha=0.3)
                    axes[i].tick_params(labelsize=8)
                    
                    # Ajouter les lignes horizontales (depth)
                    for h_line in st.session_state.h_lines:
                        axes[i].axhline(y=h_line, color=line_color_h, linestyle='--', 
                                    linewidth=line_width, alpha=0.7, label=f'Depth={h_line}' if i == 0 else '')
                    
                    # Ajouter les lignes verticales (valeurs log)
                    for v_line in st.session_state.v_lines:
                        # Vérifier que la ligne verticale est dans la plage du log
                        if col_min <= v_line <= col_max:
                            axes[i].axvline(x=v_line, color=line_color_v, linestyle='--', 
                                        linewidth=line_width, alpha=0.7)
            
                axes[0].set_ylabel('Depth (m)', fontsize=10, fontweight='bold')
                
                # Ajouter une légende si des lignes horizontales existent
                if st.session_state.h_lines:
                    axes[0].legend(loc='best', fontsize=8)
                
                plt.suptitle(f'{group_name} - Row {row + 1}', fontsize=12, fontweight='bold')
                plt.tight_layout()
            
                st.pyplot(fig)
                plt.close(fig)
        
            st.divider()

    # Section de gestion des lignes
    st.markdown("---")
    st.markdown("### 📋 Gestion complète des lignes de référence")

    col_h_list, col_v_list = st.columns(2)

    with col_h_list:
        st.markdown(f"#### 🔴 Lignes horizontales - Depth ({len(st.session_state.h_lines)})")
        if st.session_state.h_lines:
            sorted_h = sorted(st.session_state.h_lines, reverse=True)
            for i, val in enumerate(sorted_h):
                cols = st.columns([3, 1, 1])
                cols[0].markdown(f"**Depth = {val:.2f}**")
                
                if cols[1].button("❌", key=f"del_h_{i}_{val}"):
                    st.session_state.h_lines.remove(val)
                    st.rerun()
                
                if cols[2].button("✏️", key=f"edit_h_{i}_{val}"):
                    st.session_state[f"editing_h_{val}"] = True
                
                if st.session_state.get(f"editing_h_{val}", False):
                    new_val = st.number_input(
                        f"Nouvelle valeur pour Depth={val}:",
                        value=val,
                        step=1.0,
                        key=f"new_h_{i}_{val}"
                    )
                    col_save, col_cancel = st.columns(2)
                    if col_save.button("💾", key=f"save_h_{i}_{val}"):
                        st.session_state.h_lines.remove(val)
                        st.session_state.h_lines.append(round(new_val, 2))
                        st.session_state[f"editing_h_{val}"] = False
                        st.rerun()
                    if col_cancel.button("↩️", key=f"cancel_h_{i}_{val}"):
                        st.session_state[f"editing_h_{val}"] = False
                        st.rerun()
        else:
            st.info("Aucune ligne horizontale")
        
        if st.session_state.h_lines and st.button("🗑️ Supprimer toutes les lignes H", key="del_all_h"):
            st.session_state.h_lines = []
            st.rerun()

    with col_v_list:
        st.markdown(f"#### 🟢 Lignes verticales - Valeurs log ({len(st.session_state.v_lines)})")
        if st.session_state.v_lines:
            sorted_v = sorted(st.session_state.v_lines)
            for i, val in enumerate(sorted_v):
                cols = st.columns([3, 1, 1])
                cols[0].markdown(f"**Valeur = {val:.2f}**")
                
                if cols[1].button("❌", key=f"del_v_{i}_{val}"):
                    st.session_state.v_lines.remove(val)
                    st.rerun()
                
                if cols[2].button("✏️", key=f"edit_v_{i}_{val}"):
                    st.session_state[f"editing_v_{val}"] = True
                
                if st.session_state.get(f"editing_v_{val}", False):
                    new_val = st.number_input(
                        f"Nouvelle valeur pour Valeur={val}:",
                        value=val,
                        step=1.0,
                        key=f"new_v_{i}_{val}"
                    )
                    col_save, col_cancel = st.columns(2)
                    if col_save.button("💾", key=f"save_v_{i}_{val}"):
                        st.session_state.v_lines.remove(val)
                        st.session_state.v_lines.append(round(new_val, 2))
                        st.session_state[f"editing_v_{val}"] = False
                        st.rerun()
                    if col_cancel.button("↩️", key=f"cancel_v_{i}_{val}"):
                        st.session_state[f"editing_v_{val}"] = False
                        st.rerun()
        else:
            st.info("Aucune ligne verticale")
        
        if st.session_state.v_lines and st.button("🗑️ Supprimer toutes les lignes V", key="del_all_v"):
            st.session_state.v_lines = []
            st.rerun()

    # Export des données
    st.sidebar.markdown("---")
    st.sidebar.header("📥 Export")


    export_data = {
        "uuid": my_uuid,
        "Status": status,
        "field": field,
        "other_field": other_field,
        "years": years,
        "confidence": confidence,
        "lignes_horizontales (Depth)": st.session_state.h_lines,
        "lignes_verticales (Log Values)": st.session_state.v_lines
    }

    # Afficher les données
    st.sidebar.json(export_data)

    # Bouton de téléchargement JSON
    json_str = json.dumps(export_data, indent=2)
    st.sidebar.download_button(
        label="💾 Télécharger JSON",
        data=json_str,
        file_name="lignes_graph.json",
        mime="application/json"
    )

    # # Bouton de téléchargement CSV
    # csv_data = "Type,Valeur\n"
    # for h_line in st.session_state.h_lines:
    #     csv_data += f"Horizontal Depth,{h_line}\n"
    # for v_line in st.session_state.v_lines:
    #     csv_data += f"Vertical Log Value,{v_line}\n"

    # st.sidebar.download_button(
    #     label="📋 Télécharger CSV",
    #     data=csv_data,
    #     file_name="lignes_graph.csv",
    #     mime="text/csv"
    # )

    # Afficher un résumé
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Résumé")
    st.sidebar.metric("Lignes horizontales", len(st.session_state.h_lines))
    st.sidebar.metric("Lignes verticales", len(st.session_state.v_lines))

    st.success("✓ Well log visualization loaded!")




if __name__ == "__main__":
    main()
