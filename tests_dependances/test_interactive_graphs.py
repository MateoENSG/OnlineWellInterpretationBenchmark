import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Graphiques Interactifs", layout="wide")

st.title("📊 Graphiques Interactifs avec Lignes")

# Initialiser l'état de session
if 'h_lines' not in st.session_state:
    st.session_state.h_lines = []
if 'v_lines' not in st.session_state:
    st.session_state.v_lines = []

# Générer des données d'exemple
np.random.seed(42)
x = np.linspace(0, 10, 100)
y = np.sin(x) * np.exp(-x/10) + 2 + np.random.normal(0, 0.1, 100)

# Calculer les limites
x_min, x_max = float(x.min()), float(x.max())
y_min, y_max = float(y.min()), float(y.max())

# Sidebar pour les options
st.sidebar.header("⚙️ Options")

line_color_h = st.sidebar.color_picker("Couleur lignes horizontales", "#FF0000")
line_color_v = st.sidebar.color_picker("Couleur lignes verticales", "#00FF00")
line_width = st.sidebar.slider("Épaisseur des lignes", 1, 5, 2)

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("🗑️ Effacer tout", use_container_width=True):
        st.session_state.h_lines = []
        st.session_state.v_lines = []
        st.rerun()

with col2:
    show_grid = st.checkbox("Grille", value=True)

# Fonction pour créer le graphique
def create_figure(h_lines, v_lines):
    fig = go.Figure()
    
    # Ajouter la courbe principale
    fig.add_trace(go.Scatter(
        x=x, 
        y=y,
        mode='lines+markers',
        name='Données',
        line=dict(color='royalblue', width=2),
        marker=dict(size=4),
        hovertemplate='x=%{x:.2f}<br>y=%{y:.2f}<extra></extra>'
    ))
    
    # Ajouter les lignes horizontales
    for h_line in h_lines:
        fig.add_hline(
            y=h_line,
            line_dash="dash",
            line_color=line_color_h,
            line_width=line_width,
            annotation_text=f"y={h_line:.2f}",
            annotation_position="right"
        )
    
    # Ajouter les lignes verticales
    for v_line in v_lines:
        fig.add_vline(
            x=v_line,
            line_dash="dash",
            line_color=line_color_v,
            line_width=line_width,
            annotation_text=f"x={v_line:.2f}",
            annotation_position="top"
        )
    
    fig.update_layout(
        title="Graphique avec lignes de référence",
        xaxis_title="X",
        yaxis_title="Y",
        hovermode='closest',
        height=500,
        showlegend=True,
        plot_bgcolor='white',
        xaxis=dict(
            gridcolor='lightgray' if show_grid else 'white',
            range=[x_min - 0.5, x_max + 0.5]
        ),
        yaxis=dict(
            gridcolor='lightgray' if show_grid else 'white',
            range=[y_min - 0.5, y_max + 0.5]
        )
    )
    
    return fig

# Layout principal en deux colonnes
col_graph, col_controls = st.columns([2, 1])

with col_graph:
    st.markdown("### 📈 Graphique")
    fig = create_figure(st.session_state.h_lines, st.session_state.v_lines)
    st.plotly_chart(fig, use_container_width=True, key="main_plot")

with col_controls:
    st.markdown("### ➕ Ajouter des lignes")
    
    # Tabs pour séparer les deux types de lignes
    tab_h, tab_v = st.tabs(["🔴 Horizontales", "🟢 Verticales"])
    
    with tab_h:
        st.markdown("#### Ligne horizontale")
        
        # Slider pour positionner la ligne
        slider_y = st.slider(
            "Position Y",
            min_value=y_min - 0.5,
            max_value=y_max + 0.5,
            value=float(np.mean(y)),
            step=0.05,
            key="slider_y",
            help="Déplacez le slider pour positionner la ligne"
        )
        
        # Aperçu de la valeur
        st.info(f"📍 Valeur: **y = {slider_y:.2f}**")
        
        # Bouton d'ajout
        if st.button("➕ Ajouter cette ligne horizontale", use_container_width=True, key="add_h"):
            if not any(abs(slider_y - existing) < 0.01 for existing in st.session_state.h_lines):
                st.session_state.h_lines.append(round(slider_y, 2))
                st.success(f"✅ Ligne ajoutée: y={slider_y:.2f}")
                st.rerun()
            else:
                st.warning("⚠️ Cette ligne existe déjà")
        
        # Ou ajout par valeur exacte
        with st.expander("✏️ Entrer une valeur exacte"):
            exact_y = st.number_input(
                "Valeur Y exacte:",
                min_value=y_min - 1,
                max_value=y_max + 1,
                value=2.0,
                step=0.1,
                key="exact_y"
            )
            if st.button("Ajouter", key="add_exact_h"):
                if not any(abs(exact_y - existing) < 0.01 for existing in st.session_state.h_lines):
                    st.session_state.h_lines.append(round(exact_y, 2))
                    st.success(f"✅ Ligne ajoutée: y={exact_y:.2f}")
                    st.rerun()
    
    with tab_v:
        st.markdown("#### Ligne verticale")
        
        # Slider pour positionner la ligne
        slider_x = st.slider(
            "Position X",
            min_value=x_min - 0.5,
            max_value=x_max + 0.5,
            value=float(np.mean(x)),
            step=0.05,
            key="slider_x",
            help="Déplacez le slider pour positionner la ligne"
        )
        
        # Aperçu de la valeur
        st.info(f"📍 Valeur: **x = {slider_x:.2f}**")
        
        # Bouton d'ajout
        if st.button("➕ Ajouter cette ligne verticale", use_container_width=True, key="add_v"):
            if not any(abs(slider_x - existing) < 0.01 for existing in st.session_state.v_lines):
                st.session_state.v_lines.append(round(slider_x, 2))
                st.success(f"✅ Ligne ajoutée: x={slider_x:.2f}")
                st.rerun()
            else:
                st.warning("⚠️ Cette ligne existe déjà")
        
        # Ou ajout par valeur exacte
        with st.expander("✏️ Entrer une valeur exacte"):
            exact_x = st.number_input(
                "Valeur X exacte:",
                min_value=x_min - 1,
                max_value=x_max + 1,
                value=5.0,
                step=0.1,
                key="exact_x"
            )
            if st.button("Ajouter", key="add_exact_v"):
                if not any(abs(exact_x - existing) < 0.01 for existing in st.session_state.v_lines):
                    st.session_state.v_lines.append(round(exact_x, 2))
                    st.success(f"✅ Ligne ajoutée: x={exact_x:.2f}")
                    st.rerun()

# Section de gestion des lignes
st.markdown("---")
st.markdown("### 📋 Gestion des lignes")

col_h_list, col_v_list = st.columns(2)

with col_h_list:
    st.markdown(f"#### 🔴 Lignes horizontales ({len(st.session_state.h_lines)})")
    if st.session_state.h_lines:
        # Trier les lignes
        sorted_h = sorted(st.session_state.h_lines, reverse=True)
        for i, val in enumerate(sorted_h):
            cols = st.columns([3, 1, 1])
            cols[0].markdown(f"**y = {val:.2f}**")
            
            # Bouton pour supprimer
            if cols[1].button("❌", key=f"del_h_{i}_{val}", help="Supprimer"):
                st.session_state.h_lines.remove(val)
                st.rerun()
            
            # Bouton pour éditer
            if cols[2].button("✏️", key=f"edit_h_{i}_{val}", help="Éditer"):
                st.session_state[f"editing_h_{val}"] = True
                st.rerun()
            
            # Mode édition
            if st.session_state.get(f"editing_h_{val}", False):
                new_val = st.number_input(
                    f"Nouvelle valeur pour y={val}:",
                    value=val,
                    step=0.1,
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
    st.markdown(f"#### 🟢 Lignes verticales ({len(st.session_state.v_lines)})")
    if st.session_state.v_lines:
        # Trier les lignes
        sorted_v = sorted(st.session_state.v_lines)
        for i, val in enumerate(sorted_v):
            cols = st.columns([3, 1, 1])
            cols[0].markdown(f"**x = {val:.2f}**")
            
            # Bouton pour supprimer
            if cols[1].button("❌", key=f"del_v_{i}_{val}", help="Supprimer"):
                st.session_state.v_lines.remove(val)
                st.rerun()
            
            # Bouton pour éditer
            if cols[2].button("✏️", key=f"edit_v_{i}_{val}", help="Éditer"):
                st.session_state[f"editing_v_{val}"] = True
                st.rerun()
            
            # Mode édition
            if st.session_state.get(f"editing_v_{val}", False):
                new_val = st.number_input(
                    f"Nouvelle valeur pour x={val}:",
                    value=val,
                    step=0.1,
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
if st.sidebar.button("Exporter les lignes", use_container_width=True):
    export_data = {
        "lignes_horizontales": st.session_state.h_lines,
        "lignes_verticales": st.session_state.v_lines
    }
    st.sidebar.json(export_data)
    st.sidebar.download_button(
        label="💾 Télécharger JSON",
        data=str(export_data),
        file_name="lignes_graph.json",
        mime="application/json"
    )