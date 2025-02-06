import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image
import base64
import ast
import numpy as np
import plotly.graph_objects as go
import io
import streamlit.components.v1 as components

texts = {
    "en": {
        # Page Titles and Headers
        "page_title": "Car Comparator",
        "title_select_brand": "Brand",
        "title_select_model": "Model",
        "title_select_year": "Year",
        "title_select_transmission": "Transmission",
        "title_select_fuel": "Fuel",
        "title_select_emission": "Emission",
        "title_select_power": "Power (HP)",
        "title_select_mileage": "Mileage",
        "radial_axis_range": "Radial Axis Range",
        "image_not_available": "Image not available",
        
        # No Data Messages
        "no_brands_available": "No brands available.",
        "no_models_available": "No models available for this brand.",
        "no_years_available": "No years available for this model.",
        "no_transmissions_available": "No transmissions available for this year.",
        "no_fuels_available": "No fuels available for this transmission.",
        "no_emissions_available": "No emissions available for this fuel.",
        "no_powers_available": "No power options available for this emission.",
        "no_mileages_available": "No mileage options available for this power.",
        "no_valid_columns_radar_chart": "No valid columns to create the radar chart.",
        "no_data_for_both_cars": "No data found for both selected cars.",
        
        # Radar Chart Labels
        "price": "Price",
        "mileage": "Mileage",
        "power_hp": "Power (HP)",
        "max_speed": "Max Speed",
        "acceleration": "Acceleration",
        "average_consumption": "Average Consumption",
        "weight": "Weight",
        "trunk_capacity": "Trunk Capacity",
        
        # Other UI Elements
        "save_cache_button": "Clear Cache",
        "filter_title": "Filters"
    },
    "es": {
        # Page Titles and Headers
        "page_title": "Comparador de coches",
        "title_select_brand": "Marca",
        "title_select_model": "Modelo",
        "title_select_year": "Año",
        "title_select_transmission": "Cambio",
        "title_select_fuel": "Combustible",
        "title_select_emission": "Distintivo",
        "title_select_power": "Potencia (CV)",
        "title_select_mileage": "Kilometraje",
        "radial_axis_range": "Rango del eje radial",
        "image_not_available": "Imagen no disponible",
        
        # No Data Messages
        "no_brands_available": "No hay marcas disponibles.",
        "no_models_available": "No hay modelos disponibles para esta marca.",
        "no_years_available": "No hay años disponibles para este modelo.",
        "no_transmissions_available": "No hay tipos de cambio disponibles para este año.",
        "no_fuels_available": "No hay combustibles disponibles para este cambio.",
        "no_emissions_available": "No hay distintivos disponibles para este combustible.",
        "no_powers_available": "No hay potencias disponibles para este distintivo.",
        "no_mileages_available": "No hay kilometrajes disponibles para esta potencia.",
        "no_valid_columns_radar_chart": "No hay columnas válidas para crear el gráfico de radar.",
        "no_data_for_both_cars": "No se encontraron datos para ambos coches seleccionados.",
        
        # Radar Chart Labels
        "price": "Precio",
        "mileage": "Kilometraje",
        "power_hp": "Potencia (CV)",
        "max_speed": "Velocidad Máxima",
        "acceleration": "Aceleración",
        "average_consumption": "Consumo Medio",
        "weight": "Peso",
        "trunk_capacity": "Capacidad Maletero",
        
        # Other UI Elements
        "save_cache_button": "Limpiar Caché",
        "filter_title": "Filtros"
    }
}

# Selector de idioma en la barra lateral
idioma = st.sidebar.radio(
    'Language',  
    ("English", "Español") 
)

# Configuración inicial del idioma
if 'lang' not in st.session_state:
    st.session_state.lang = "en" 

# Actualizar el estado del idioma según la selección
if idioma == "Español":
    st.session_state.lang = "es"
else:
    st.session_state.lang = "en"

lang = st.session_state.lang

def convertir_str_a_bytes(valor):
    # Verificamos que el valor sea una cadena y que parezca la representación de bytes (comienza con "b'")
    if isinstance(valor, str) and valor.startswith("b'"):
        try:
            return ast.literal_eval(valor)
        except Exception as e:
            print(f"Error al evaluar la cadena: {e}")
            return None
    return valor

# Función para convertir datos binarios a imagen
def convertir_binario_a_imagen(binario):
    if binario is not None:
        return Image.open(BytesIO(binario))
    else:
        return None
    
def imagen_to_base64(imagen):
    buffered = BytesIO()
    imagen.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def mostrar_coche(imagen):
    if imagen:
        imagen_base64 = imagen_to_base64(imagen)
        st.markdown(
            f"""
            <div style="
                display: flex; 
                justify-content: center; 
                align-items: center; 
                margin-bottom: 10px; 
                height: 350px; /* Establece la altura fija del contenedor */
            ">
                <img src="data:image/png;base64,{imagen_base64}" style="
                    max-width: 100%; 
                    max-height: 100%; 
                    object-fit: contain; /* Ajusta la imagen dentro del contenedor sin deformarla */
                ">
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Mostrar un marcador de "Imagen no disponible" con la misma altura fija
        st.markdown(
            """
            <div style="
                display: flex; 
                justify-content: center; 
                align-items: center; 
                margin-bottom: 20px; 
                height: 350px; /* Misma altura fija que el contenedor de la imagen */
                background-color: #f0f0f0; 
                border: 1px solid #ccc; 
                border-radius: 5px;
            ">
                <p style="text-align: center; font-size: 16px; color: #555;">Imagen no disponible</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("""
    <style>
    /* Reducir márgenes de los selectores y centrarlos */
    div[data-baseweb="select"] {
        width: 135px !important; /* Mantener ancho uniforme */
        margin: 5px auto !important; /* Centrar selectores */
    }

    /* Reducir espacio entre el título y el selector y centrar títulos */
    p.titulo-select {
        margin-bottom: 1px !important; /* Controlar el margen inferior del título */
        text-align: center !important; /* Centrar texto del título */
    }

    /* Centrar otros elementos dentro de las columnas */
    [data-testid="stVerticalBlock"] .stColumn > div {
        align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Cargar datos
@st.cache_data
def load_data():
    # Lista de nombres de archivo para los 10 CSV
    files = [f"bin/datos_img_completos_{i}.csv" for i in range(1, 11)]
    
    # Leer cada archivo y almacenar en una lista de DataFrames
    dfs = [pd.read_csv(file) for file in files]
    
    # Concatenar todos los DataFrames en uno solo
    df = pd.concat(dfs, ignore_index=True)
    
    # Convertir la columna 'foto_binaria' de str a bytes (si es necesario)
    df["foto_binaria"] = df["foto_binaria"].apply(convertir_str_a_bytes)
    
    # Reemplazar valores nulos en columnas categóricas
    columnas_categoricas = ['marca', 'modelo', 'tipo_cambio', 'combustible', 'distintivo_ambiental']
    df[columnas_categoricas] = df[columnas_categoricas].fillna('Desconocido')
    
    # Asegurar que las columnas numéricas sean de tipo numérico
    columnas_numericas = ['precio_contado', 'kilometraje', 'potencia_cv', 'velocidad_max', 
                          'aceleracion', 'consumo_medio', 'peso', 'capacidad_maletero']
    df[columnas_numericas] = df[columnas_numericas].apply(pd.to_numeric, errors='coerce')
    df[columnas_numericas] = df[columnas_numericas].fillna(0)
    
    return df

df = load_data()

# Título de la página
st.markdown(f"<h1 style='text-align: center;font-size: 3rem;'>{texts[lang]['page_title']}</h1>", unsafe_allow_html=True)

# Dividir en 5 columnas principales
col1, col2, col3, col4, col5 = st.columns([1, 4, 1, 4, 1])

# Columna vacía (espacio a la izquierda)
with col1:
    st.empty()

# Filtros para el Coche 1
with col2:
    # Crear un marcador de posición para el título
    title_placeholder1 = st.empty()

    # Primera fila de filtros
    fila1_coche1 = st.columns(4)
    with fila1_coche1[0]:
        st.markdown(f"<p class='titulo-select'>{texts[lang]['title_select_brand']}</p>", unsafe_allow_html=True)
        marcas_disponibles = df["marca"].unique()
        marcas_disponibles = sorted([marca for marca in marcas_disponibles if str(marca).lower() != "desconocido"])
        if len(marcas_disponibles) > 0:
            marca1 = st.selectbox("Marca", marcas_disponibles, key="marca1", label_visibility="collapsed", index=0)
        else:
            st.write(texts[lang]['no_brands_available'])
            st.stop()
    with fila1_coche1[1]:
        st.markdown(f"<p class='titulo-select'>{texts[lang]['title_select_model']}</p>", unsafe_allow_html=True)
        modelos_disponibles = df[df["marca"] == marca1]["modelo"].sort_values().unique()
        if len(modelos_disponibles) > 0:
            modelo1 = st.selectbox("Modelo", modelos_disponibles, key="modelo1", label_visibility="collapsed", index=0)
        else:
            st.write(texts[lang]['no_models_available'])
            st.stop()
    with fila1_coche1[2]:
        st.markdown(f"<p class='titulo-select'>{texts[lang]['title_select_year']}</p>", unsafe_allow_html=True)
        anos_disponibles = df[(df["marca"] == marca1) & (df["modelo"] == modelo1)]["ano_matriculacion"].sort_values().unique()
        if len(anos_disponibles) > 0:
            ano1 = st.selectbox("Año", anos_disponibles, key="ano1", label_visibility="collapsed", index=0)
        else:
            st.write(texts[lang]['no_years_available'])
            st.stop()
    with fila1_coche1[3]:
        st.markdown(f"<p class='titulo-select'>{texts[lang]['title_select_transmission']}</p>", unsafe_allow_html=True)
        cambios_disponibles = df[
            (df["marca"] == marca1) &
            (df["modelo"] == modelo1) &
            (df["ano_matriculacion"] == ano1)
        ]["tipo_cambio"].sort_values().unique()
        if len(cambios_disponibles) > 0:
            tipo_cambio1 = st.selectbox("Tipo cambio", cambios_disponibles, key="tipo_cambio1", label_visibility="collapsed", index=0)
        else:
            st.write(texts[lang]['no_transmissions_available'])
            st.stop()

    # Segunda fila de filtros
    fila2_coche1 = st.columns(4)
    with fila2_coche1[0]:
        st.markdown(f"<p class='titulo-select'>{texts[lang]['title_select_fuel']}</p>", unsafe_allow_html=True)
        combustibles_disponibles = df[
            (df["marca"] == marca1) &
            (df["modelo"] == modelo1) &
            (df["ano_matriculacion"] == ano1) &
            (df["tipo_cambio"] == tipo_cambio1)
        ]["combustible"].sort_values().unique()
        if len(combustibles_disponibles) > 0:
            combustible1 = st.selectbox("Combustible", combustibles_disponibles, key="combustible1", label_visibility="collapsed", index=0)
        else:
            st.write(texts[lang]['no_fuels_available']) 
    with fila2_coche1[1]:
        st.markdown(f"<p class='titulo-select'>{texts[lang]['title_select_emission']}</p>", unsafe_allow_html=True)
        distintivos_disponibles = df[
            (df["marca"] == marca1) &
            (df["modelo"] == modelo1) &
            (df["ano_matriculacion"] == ano1) &
            (df["tipo_cambio"] == tipo_cambio1) &
            (df["combustible"] == combustible1)
        ]["distintivo_ambiental"].sort_values().unique()
        if len(distintivos_disponibles) > 0:
            distintivo1 = st.selectbox("Distintivo", distintivos_disponibles, key="distintivo1", label_visibility="collapsed", index=0)
        else:
            st.write(texts[lang]['no_emissions_available']) 
    with fila2_coche1[2]:
        st.markdown(f"<p class='titulo-select'>{texts[lang]['title_select_power']}</p>", unsafe_allow_html=True)
        potencias_disponibles = df[
            (df["marca"] == marca1) &
            (df["modelo"] == modelo1) &
            (df["ano_matriculacion"] == ano1) &
            (df["tipo_cambio"] == tipo_cambio1) &
            (df["combustible"] == combustible1) &
            (df["distintivo_ambiental"] == distintivo1)
        ]["potencia_cv"].sort_values().unique()
        if len(potencias_disponibles) > 0:
            potencia1 = st.selectbox("Potencia", potencias_disponibles, key="potencia1", label_visibility="collapsed", index=0)
        else:
            st.write(texts[lang]['no_powers_available']) 
            st.stop()
    with fila2_coche1[3]:
        st.markdown(f"<p class='titulo-select'>{texts[lang]['title_select_mileage']}</p>", unsafe_allow_html=True)
        kilometrajes_disponibles = df[
            (df["marca"] == marca1) &
            (df["modelo"] == modelo1) &
            (df["ano_matriculacion"] == ano1) &
            (df["tipo_cambio"] == tipo_cambio1) &
            (df["combustible"] == combustible1) &
            (df["distintivo_ambiental"] == distintivo1) &
            (df["potencia_cv"] == potencia1)
        ]["kilometraje"].sort_values().unique()
        if len(kilometrajes_disponibles) > 0:
            kilometraje1 = st.selectbox("Kilometraje", kilometrajes_disponibles, key="kilometraje1", label_visibility="collapsed", index=0)
        else:
            st.write(texts[lang]['no_mileages_available']) 
            st.stop()

    # Actualizar el título con la marca y modelo seleccionados
    title_placeholder1.markdown(f"<h3 style='text-align: center;'>{marca1} {modelo1}</h3>", unsafe_allow_html=True)

    # Mostrar imagen debajo de los filtros
    df_filtrado1 = df[
        (df["marca"] == marca1)
        & (df["modelo"] == modelo1)
        & (df["ano_matriculacion"] == ano1)
        & (df["tipo_cambio"] == tipo_cambio1)
        & (df["combustible"] == combustible1)
        & (df["distintivo_ambiental"] == distintivo1)
        & (df["potencia_cv"] == potencia1)
        & (df["kilometraje"] == kilometraje1)
    ].copy().head(1)

    

    if not df_filtrado1.empty:
        datos_coche1 = df_filtrado1.iloc[0]
        foto_binaria = datos_coche1["foto_binaria"]

        try: 
            imagen1 = convertir_binario_a_imagen(foto_binaria)
        except Exception as e:
            print(f"Error al cargar la imagen del coche 1: {e}")
            imagen1 = None

        mostrar_coche(imagen1)
        
    else:
        st.write(f"No se encontraron datos para el {marca1} {modelo1} ({ano1}) con los filtros seleccionados.")

# Columna vacía (espacio entre los coches)
with col3:
    st.empty()

# Filtros para el Coche 2
with col4:
    # Crear un marcador de posición para el título
    title_placeholder2 = st.empty()

    # Primera fila de filtros
    fila1_coche2 = st.columns(4)
    with fila1_coche2[0]:
        st.markdown(f"<p class='titulo-select'>{texts[lang]['title_select_brand']}</p>", unsafe_allow_html=True)
        marcas_disponibles = df["marca"].sort_values().unique()
        if len(marcas_disponibles) > 0:
            marca2 = st.selectbox("Marca", marcas_disponibles, key="marca2", label_visibility="collapsed", index=0)
        else:
            st.write(texts[lang]['no_brands_available'])
            st.stop()
    with fila1_coche2[1]:
        st.markdown(f"<p class='titulo-select'>{texts[lang]['title_select_model']}</p>", unsafe_allow_html=True)
        modelos_disponibles = df[df["marca"] == marca2]["modelo"].sort_values().unique()
        if len(modelos_disponibles) > 0:
            modelo2 = st.selectbox("Modelo", modelos_disponibles, key="modelo2", label_visibility="collapsed", index=0)
        else:
            st.write(texts[lang]['no_models_available'])
            st.stop()
    with fila1_coche2[2]:
        st.markdown(f"<p class='titulo-select'>{texts[lang]['title_select_year']}</p>", unsafe_allow_html=True)
        anos_disponibles = df[(df["marca"] == marca2) & (df["modelo"] == modelo2)]["ano_matriculacion"].sort_values().unique()
        if len(anos_disponibles) > 0:
            ano2 = st.selectbox("Año", anos_disponibles, key="ano2", label_visibility="collapsed", index=0)
        else:
            st.write(texts[lang]['no_years_available'])
            st.stop()
    with fila1_coche2[3]:
        st.markdown(f"<p class='titulo-select'>{texts[lang]['title_select_transmission']}</p>", unsafe_allow_html=True)
        cambios_disponibles = df[
            (df["marca"] == marca2) &
            (df["modelo"] == modelo2) &
            (df["ano_matriculacion"] == ano2)
        ]["tipo_cambio"].sort_values().unique()
        if len(cambios_disponibles) > 0:
            tipo_cambio2 = st.selectbox("Tipo cambio", cambios_disponibles, key="tipo_cambio2", label_visibility="collapsed", index=0)
        else:
            st.write(texts[lang]['no_transmissions_available'])
            st.stop()

    # Segunda fila de filtros
    fila2_coche2 = st.columns(4)
    with fila2_coche2[0]:
        st.markdown(f"<p class='titulo-select'>{texts[lang]['title_select_fuel']}</p>", unsafe_allow_html=True)
        combustibles_disponibles = df[
            (df["marca"] == marca2) &
            (df["modelo"] == modelo2) &
            (df["ano_matriculacion"] == ano2) &
            (df["tipo_cambio"] == tipo_cambio2)
        ]["combustible"].sort_values().unique()
        if len(combustibles_disponibles) > 0:
            combustible2 = st.selectbox("Combustible", combustibles_disponibles, key="combustible2", label_visibility="collapsed", index=0)
        else:
            st.write(texts[lang]['no_fuels_available'])
    with fila2_coche2[1]:
        st.markdown(f"<p class='titulo-select'>{texts[lang]['title_select_emission']}</p>", unsafe_allow_html=True)
        distintivos_disponibles = df[
            (df["marca"] == marca2) &
            (df["modelo"] == modelo2) &
            (df["ano_matriculacion"] == ano2) &
            (df["tipo_cambio"] == tipo_cambio2) &
            (df["combustible"] == combustible2)
        ]["distintivo_ambiental"].sort_values().unique()
        if len(distintivos_disponibles) > 0:
            distintivo2 = st.selectbox("Distintivo", distintivos_disponibles, key="distintivo2", label_visibility="collapsed", index=0)
        else:
            st.write(texts[lang]['no_emissions_available'])
    with fila2_coche2[2]:
        st.markdown(f"<p class='titulo-select'>{texts[lang]['title_select_power']}</p>", unsafe_allow_html=True)
        potencias_disponibles = df[
            (df["marca"] == marca2) &
            (df["modelo"] == modelo2) &
            (df["ano_matriculacion"] == ano2) &
            (df["tipo_cambio"] == tipo_cambio2) &
            (df["combustible"] == combustible2) &
            (df["distintivo_ambiental"] == distintivo2)
        ]["potencia_cv"].sort_values().unique()
        if len(potencias_disponibles) > 0:
            potencia2 = st.selectbox("Potencia", potencias_disponibles, key="potencia2", label_visibility="collapsed", index=0)
        else:
            st.write(texts[lang]['no_powers_available'])
            st.stop()
    with fila2_coche2[3]:
        st.markdown(f"<p class='titulo-select'>{texts[lang]['title_select_mileage']}</p>", unsafe_allow_html=True)
        kilometrajes_disponibles = df[
            (df["marca"] == marca2) &
            (df["modelo"] == modelo2) &
            (df["ano_matriculacion"] == ano2) &
            (df["tipo_cambio"] == tipo_cambio2) &
            (df["combustible"] == combustible2) &
            (df["distintivo_ambiental"] == distintivo2) &
            (df["potencia_cv"] == potencia2)
        ]["kilometraje"].sort_values().unique()
        if len(kilometrajes_disponibles) > 0:
            kilometraje2 = st.selectbox("Kilometraje", kilometrajes_disponibles, key="kilometraje2", label_visibility="collapsed", index=0)
        else:
            st.write(texts[lang]['no_mileages_available'])
            st.stop()

    # Actualizar el título con la marca y modelo seleccionados
    title_placeholder2.markdown(f"<h3 style='text-align: center;'>{marca2} {modelo2}</h3>", unsafe_allow_html=True)

    # Mostrar imagen debajo de los filtros
    df_filtrado2 = df[
        (df["marca"] == marca2)
        & (df["modelo"] == modelo2)
        & (df["ano_matriculacion"] == ano2)
        & (df["tipo_cambio"] == tipo_cambio2)
        & (df["combustible"] == combustible2)
        & (df["distintivo_ambiental"] == distintivo2)
        & (df["potencia_cv"] == potencia2)
        & (df["kilometraje"] == kilometraje2)
    ].copy().head(1)  

    if not df_filtrado2.empty:
        datos_coche2 = df_filtrado2.iloc[0]
        foto_binaria = datos_coche2["foto_binaria"]

        try: 
            imagen2 = convertir_binario_a_imagen(foto_binaria)
        except Exception as e:
            print(f"Error al cargar la imagen del coche 2: {e}")
            imagen2 = None

        mostrar_coche(imagen2)
       
    else:
        st.write(f"No se encontraron datos para el {marca2} {modelo2} ({ano2}) con los filtros seleccionados.")

# Columna vacía (espacio a la derecha)
with col5:
    st.empty()


columnas_seleccionadas = [
    "precio_contado", "kilometraje", "potencia_cv", 
    "velocidad_max", "aceleracion", "consumo_medio", "peso", 
    "capacidad_maletero"
]

if not df_filtrado1.empty and not df_filtrado2.empty:

    # Crear copia del DataFrame con las columnas seleccionadas
    df_todos_los_coches = df[columnas_seleccionadas].copy()

    # Asegurar que las columnas numéricas son de tipo numérico
    df_todos_los_coches = df_todos_los_coches.apply(pd.to_numeric, errors='coerce')

    columnas_log = ["precio_contado", "kilometraje", "potencia_cv"]
    for col in columnas_log:
        # Reemplazar valores nulos o negativos antes de aplicar log
        df_todos_los_coches[col] = df_todos_los_coches[col].fillna(0)
        df_todos_los_coches[col] = df_todos_los_coches[col].apply(lambda x: np.log1p(x) if x >= 0 else 0)

    # Normalizar las columnas numéricas
    min_vals = {}
    max_vals = {}

    for col in df_todos_los_coches.columns:
        min_vals[col] = df_todos_los_coches[col].min()
        max_vals[col] = df_todos_los_coches[col].max()


    # Función para normalizar un DataFrame utilizando min y max
    def normalize_df(df_to_normalize, min_vals, max_vals, columnas_log):
        df_normalized = df_to_normalize.copy()
        for col in columnas_log:
            df_normalized[col] = df_normalized[col].fillna(0)
            df_normalized[col] = df_normalized[col].apply(lambda x: np.log1p(x) if x >= 0 else 0)
        for col in df_normalized.columns:
            min_val = min_vals[col]
            max_val = max_vals[col]
            if max_val - min_val != 0:
                if col not in ['aceleracion', 'consumo_medio']:
                    df_normalized[col] = (df_normalized[col] - min_val) / (max_val - min_val)
                else:
                    df_normalized[col] = (max_val - df_normalized[col]) / (max_val - min_val)
            else:
                df_normalized[col] = 0.0
        return df_normalized
    
    # Normalizar los DataFrames filtrados
    df_filtrado1_normalized = normalize_df(df_filtrado1[columnas_seleccionadas].copy(), min_vals, max_vals, columnas_log)
    df_filtrado2_normalized = normalize_df(df_filtrado2[columnas_seleccionadas].copy(), min_vals, max_vals, columnas_log)

    # Combinar los DataFrames normalizados
    df_normalizado_seleccionados = pd.concat([df_filtrado1_normalized, df_filtrado2_normalized], ignore_index=True)

    # Combinar los DataFrames originales (no normalizados) para verificar columnas válidas
    df_combinado = pd.concat([df_filtrado1[columnas_seleccionadas], df_filtrado2[columnas_seleccionadas]], ignore_index=True).copy()

    columnas_validas = [col for col in columnas_seleccionadas if (df_combinado[col] != 0).all()]

    if columnas_validas:
        # Crear un DataFrame con solo las columnas válidas y hacer una copia
        df_radar = df_normalizado_seleccionados[columnas_validas].copy()

        columnas_legibles = {
            "precio_contado": texts[lang]['price'],
            "kilometraje": texts[lang]['mileage'],
            "potencia_cv": texts[lang]['power_hp'],
            "velocidad_max": texts[lang]['max_speed'],
            "aceleracion": texts[lang]['acceleration'],
            "consumo_medio": texts[lang]['average_consumption'],
            "peso": texts[lang]['weight'],
            "capacidad_maletero": texts[lang]['trunk_capacity']
        }

        # Renombrar las columnas para que sean más legibles
        df_radar = df_radar.rename(columns=columnas_legibles)

        # Preparar los datos para el gráfico
        categorias = df_radar.columns.tolist()
        valores_coche1 = df_radar.iloc[0].tolist()  # Valores del coche 1
        valores_coche2 = df_radar.iloc[1].tolist()  # Valores del coche 2

        # Agregar el primer y último valor para cerrar el radar
        valores_coche1.append(valores_coche1[0])
        valores_coche2.append(valores_coche2[0])
        categorias.append(categorias[0])

        # Obtener los nombres personalizados para la leyenda
        nombre_coche1 = f"{df_filtrado1['marca'].iloc[0]} {df_filtrado1['modelo'].iloc[0]}"
        nombre_coche2 = f"{df_filtrado2['marca'].iloc[0]} {df_filtrado2['modelo'].iloc[0]}"

        # Crear cinco columnas de igual ancho
        col2, col4 = st.columns([3, 3])

        with col4:
            inner_col1, inner_col2, inner_col3 = st.columns([1, 5, 1])

            with inner_col1:
                st.empty()

            with inner_col2:

                # Combinar los datos de los coches seleccionados y crear una copia explícita
                df_combinado = pd.concat([df_filtrado1[columnas_seleccionadas], df_filtrado2[columnas_seleccionadas]], ignore_index=True).copy()
                df_combinado = df_combinado.replace(0,'Desconocido')

                # Obtener los nombres personalizados para las columnas (marca y modelo de los coches)
                if (df_filtrado1['marca'].iloc[0] == df_filtrado2['marca'].iloc[0]) and (df_filtrado1['modelo'].iloc[0] == df_filtrado2['modelo'].iloc[0]):
                    # Si la marca y el modelo son iguales, añadir '1' y '2'
                    nombre_coche1 = f"{df_filtrado1['marca'].iloc[0]} {df_filtrado1['modelo'].iloc[0]} 1"
                    nombre_coche2 = f"{df_filtrado2['marca'].iloc[0]} {df_filtrado2['modelo'].iloc[0]} 2"
                else:
                    # Si son diferentes, usar los nombres sin '1' y '2'
                    nombre_coche1 = f"{df_filtrado1['marca'].iloc[0]} {df_filtrado1['modelo'].iloc[0]}"
                    nombre_coche2 = f"{df_filtrado2['marca'].iloc[0]} {df_filtrado2['modelo'].iloc[0]}"

                # Transponer el dataframe y asignar los nombres de las columnas
                df_combinado_transpuesto = df_combinado.T.copy()  # Crear una copia explícita
                df_combinado_transpuesto.columns = [nombre_coche1, nombre_coche2]

                # Renombrar las filas (índice) del dataframe transpuesto sin inplace=True
                df_combinado_transpuesto = df_combinado_transpuesto.rename(index=columnas_legibles)

                # Añadir espacio vertical antes del DataFrame
                st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

                st.dataframe(df_combinado_transpuesto, use_container_width=True)

            with inner_col3: 
                st.empty()


        # Colocar el gráfico en la segunda columna
        with col2:
            # Crear un marcador de posición para el gráfico
            graph_placeholder = st.empty()

            slider_col1, slider_col2, slider_col3 = st.columns([1, 1, 1]) 

            with slider_col1:
                st.empty()  # Espacio vacío a la izquierda

            with slider_col2:
                # Añadir espacio superior para mover el slider hacia abajo
                #st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)  

                # Colocar el slider dentro de la columna central
                radial_min, radial_max = st.slider(
                    texts[lang]['radial_axis_range'], 
                    0.0, 
                    1.0, 
                    (0.0, 1.0), 
                    0.01, 
                    key='radial_slider'
                )

                # Opcional: Añadir espacio inferior para mover el slider hacia arriba
                st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)  

            with slider_col3:
                st.empty()  # Espacio vacío a la derecha

            # Crear y configurar el gráfico de radar
            fig = go.Figure()

            fig.add_trace(go.Scatterpolar(
                r=valores_coche1,
                theta=categorias,
                fill='toself',
                name=nombre_coche1,
                line=dict(color='red'),
                fillcolor='rgba(255, 0, 0, 0.3)'
            ))

            fig.add_trace(go.Scatterpolar(
                r=valores_coche2,
                theta=categorias,
                fill='toself',
                name=nombre_coche2,
                line=dict(color='green'),
                fillcolor='rgba(0, 255, 0, 0.3)'
            ))

            # Configuración del gráfico
            config = {
                "displayModeBar": False
            }

            fig.update_layout(
                dragmode=False,
                uirevision='constant',
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[radial_min, radial_max],
                        tickangle=45,
                        tickfont=dict(size=10)
                    )
                ),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    x=0.5,
                    xanchor="center",
                    y=1.20,
                    yanchor='top',
                    font=dict(size=12)
                ),
                autosize=True,
                margin=dict(l=40, r=40, t=100, b=40)
            )

            # Mostrar el gráfico en el marcador de posición
            graph_placeholder.plotly_chart(fig, use_container_width=True, config=config)

    else:
        st.write(texts[lang]['no_valid_columns_radar_chart'])
else:
    st.write(texts[lang]['no_data_for_both_cars'])
