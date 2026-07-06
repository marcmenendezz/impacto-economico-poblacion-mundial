import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64
import os

def formatear_numero(num):
    if abs(num) >= 1_000_000_000:
        return f"{num / 1_000_000_000:.2f} mil millones"
    elif abs(num) >= 1_000_000:
        return f"{num / 1_000_000:.2f} millones"
    elif abs(num) >= 1_000:
        return f"{num / 1_000:.2f} mil"
    else:
        return f"{num:.2f}"

# Configuración de la página
st.set_page_config(page_title="Impacto de la economía en la población mundial")


def imagen_base64(path_imagen):
    import base64
    with open(path_imagen, "rb") as f:
        return base64.b64encode(f.read()).decode()

if os.path.exists("banner_fijo.png"):
    banner_base64 = imagen_base64("banner_fijo.png")
    st.markdown(f"""
        <style>
        .stApp {{
            padding: 0;
            margin: 0;
        }}
        .main .block-container {{
            padding-top: 30px !important;
        }}
        .banner-wrapper {{
            width: 100vw;
            margin-left: calc(-50vw + 50%);
            margin-right: calc(-50vw + 50%);
            height: 135px;
            overflow: hidden;
            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        }}
        .banner-wrapper img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center;
            display: block;
        }}
        </style>

        <div class="banner-wrapper">
            <img src="data:image/png;base64,{banner_base64}">
        </div>
    """, unsafe_allow_html=True)
else:
    st.warning("⚠️ No se encontró el archivo banner_fijo.png")


st.markdown("""
<style>
/* Fondo del sidebar */
section[data-testid="stSidebar"] {
    background-color: #f5f7fa;
    padding: 2rem 1rem;
    border-right: 1px solid #ddd;
}

/* Título grande y destacado */
section[data-testid="stSidebar"] .stRadio > label {
    font-size: 1.5rem !important;
    font-weight: 800 !important;
    color: #1c3faa;
    margin-bottom: 1rem;
}

/* Menú estilo profesional */
.stRadio > div {
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
}

/* Opciones con tamaño uniforme y animación */
.stRadio > div > label {
    background-color: white;
    padding: 12px 16px;
    border-radius: 8px;
    border: 1px solid #ccc;
    cursor: pointer;
    font-weight: 500;
    color: #2c3e50;
    height: 48px;
    min-height: 48px;
    max-height: 48px;
    width: 100%;
    box-sizing: border-box;
    transition: all 0.25s ease-in-out;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    text-align: left;
    white-space: nowrap;
    overflow: hidden;
}

/* Igualar el ancho real (fix layout) */
section[data-testid="stSidebar"] .stRadio {
    width: 100% !important;
}

/* Hover animado */
.stRadio > div > label:hover {
    background-color: #eaf1fb;
    border-color: #1c7ed6;
    transform: scale(1.02);
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* Selección */
.stRadio > div > label[data-selected="true"] {
    background-color: #d0e6ff !important;
    border: 2px solid #1c7ed6;
    font-weight: 600;
    color: #1c3faa;
}
<style>
.menu-titulo {
    font-size: 1.6rem;
    font-weight: 800;
    color: #1c3faa;
    margin-bottom: 1.2rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
</style>

</style>
""", unsafe_allow_html=True)




# Imagen + Título único y centrado
st.markdown('<h1 style="text-align: center; font-size: 32px; color: #2c3e50;">IMPACTO DE LA ECONOMÍA EN LA POBLACIÓN MUNDIAL</h1>', unsafe_allow_html=True)

# Cargar y limpiar datos
df = pd.read_excel("data/tabla_de_datos_sin_faltantes.xlsx")
df.columns = df.columns.str.strip().str.lower()

st.sidebar.markdown('<div class="menu-titulo"> MENÚ PRINCIPAL</div>', unsafe_allow_html=True)

menu = st.sidebar.radio("", [
    "Explicación del proyecto",
    "Memoria del proyecto",
    "Ver base de datos",
    "Análisis univariable",
    "Análisis multivariable",
    "Comparación entre países"
])


if menu == "Explicación del proyecto":
    st.subheader("¿De qué trata esta web?")
    st.markdown("""
Esta aplicación interactiva forma parte del proyecto *Impacto de la economía en la población mundial*.

El objetivo de esta página web es dinamizar el análisis de diferentes variables para diverosos países. Entre estas variables, encontramos variables económicas (PIB, estructura del empleo...), indicadores demográficos y sociales (tasa de natalidad, esperanza de vida...) en 8 países entre 1993 y 2024.

Desde esta web se permite al usuario:
-  Leer la memoria del proyecto.
-  Ver la base de datos usada para este proyecto.
-  Ver cómo evoluciona una variable concreta en un país específico.
-  Analizar cómo se relacionan dos variables dentro de un mismo país.
-  Comparar el comportamiento de una variable para varios países.
    """)

elif menu == "Memoria del proyecto":
    import streamlit.components.v1 as components
    st.subheader("Memoria del proyecto")
    st.markdown("Visualiza la memoria completa justo debajo o descárgala en PDF:")

    pdf_url = "https://raw.githubusercontent.com/marcmenendezz/impacto-economia-poblacion/main/Memoria%20Proyecto.pdf"
    viewer_url = f"https://mozilla.github.io/pdf.js/web/viewer.html?file={pdf_url}"

    components.iframe(viewer_url, height=850, scrolling=True)

    # Descargar el contenido del PDF desde GitHub
    import requests

    response = requests.get(pdf_url)
    if response.status_code == 200:
        st.download_button(
            label="📥 Descargar memoria (.pdf)",
            data=response.content,
            file_name="Memoria_Proyecto.pdf",
            mime="application/pdf"
        )
    else:
        st.error("❌ No se pudo descargar la memoria en PDF desde el servidor.")

elif menu == "Análisis univariable":
    st.subheader("Análisis univariable: una variable en un país")
    pais = st.selectbox("Selecciona el país", sorted(df["country"].unique()))
    variable = st.selectbox("Selecciona la variable", [col for col in df.columns if col not in ["country", "year"]])
    df_filtrado = df[df["country"] == pais]
    st.markdown(f"### Evolución de {variable} en {pais}")
    fig, ax = plt.subplots()
    ax.plot(df_filtrado["year"], df_filtrado[variable], color="darkblue")
    ax.set_xlabel("Año")
    ax.set_ylabel(variable)
    ax.grid(True)
    ax.ticklabel_format(style='plain', axis='both', useOffset=False)
    st.pyplot(fig)
    resumen = df_filtrado[variable].describe().to_frame().T
    resumen.columns = ['Cuenta', 'Media', 'Desv. típica', 'Mínimo', '25%', 'Mediana', '75%', 'Máximo']
    resumen.index = [pais]
    resumen = resumen.applymap(formatear_numero)
    st.dataframe(resumen, use_container_width=True)

elif menu == "Análisis multivariable":
    import scipy.stats as stats
    import numpy as np
    st.subheader("Análisis multivariable: relación entre dos variables en un país")
    pais = st.selectbox("Selecciona el país", sorted(df["country"].unique()))
    var_x = st.selectbox("Variable en el eje X", [col for col in df.columns if col not in ["country", "year"]])
    var_y = st.selectbox("Variable en el eje Y", [col for col in df.columns if col not in ["country", "year"]])
    df_pais = df[df["country"] == pais][[var_x, var_y]].dropna()
    st.markdown(f"### Diagrama de dispersión de {var_y} vs {var_x} en {pais}")
    fig, ax = plt.subplots()
    x = df_pais[var_x].to_numpy().flatten()
    y = df_pais[var_y].to_numpy().flatten()
    ax.scatter(x, y, color='#228B22', label='Datos')
    coef = np.polyfit(x, y, 1)
    poly_fn = np.poly1d(coef)
    ax.plot(x, poly_fn(x), color='#66BB66', linestyle="--", label='Regresión lineal')
    ax.set_xlabel(var_x)
    ax.set_ylabel(var_y)
    ax.grid(True)
    ax.legend()
    ax.ticklabel_format(style='plain', axis='both', useOffset=False)
    st.pyplot(fig)
    r, p = stats.pearsonr(x, y)
    resumen = pd.DataFrame({
        "Coef. Pearson (r)": [round(r, 3)],
        "p-valor": [round(p, 4)],
        f"Media {var_x}": [round(np.mean(x), 2)],
        f"Media {var_y}": [round(np.mean(y), 2)],
        "n (muestras)": [len(x)]
    })
    resumen = resumen.applymap(formatear_numero)
    st.dataframe(resumen, use_container_width=True)

elif menu == "Comparación entre países":
    st.subheader("Comparación de una variable entre dos países")
    pais1 = st.selectbox("Selecciona el primer país", sorted(df["country"].unique()), key="pais1")
    pais2 = st.selectbox("Selecciona el segundo país", sorted(df["country"].unique()), key="pais2")
    variable = st.selectbox("Variable a comparar", [col for col in df.columns if col not in ["country", "year"]])
    df_p1 = df[df["country"] == pais1]
    df_p2 = df[df["country"] == pais2]
    st.markdown(f"### Evolución de {variable} en {pais1} y {pais2}")
    fig, ax = plt.subplots()
    ax.plot(df_p1["year"], df_p1[variable], color="darkblue", label=pais1)
    ax.plot(df_p2["year"], df_p2[variable], color="firebrick", label=pais2)
    ax.set_xlabel("Año")
    ax.set_ylabel(variable)
    ax.grid(True)
    ax.legend(title="País")
    ax.ticklabel_format(style='plain', axis='both', useOffset=False)
    st.pyplot(fig)
    resumen_comp = pd.DataFrame({
        "País": [pais1, pais2],
        "Media": [df_p1[variable].mean(), df_p2[variable].mean()],
        "Mínimo": [df_p1[variable].min(), df_p2[variable].min()],
        "Máximo": [df_p1[variable].max(), df_p2[variable].max()],
        "Desv. Típica": [df_p1[variable].std(), df_p2[variable].std()],
        "n": [df_p1[variable].count(), df_p2[variable].count()]
    })
    resumen_comp.iloc[:, 1:] = resumen_comp.iloc[:, 1:].applymap(formatear_numero)
    st.dataframe(resumen_comp, use_container_width=True)

elif menu == "Ver base de datos":
    st.subheader("Base de datos completa")
    st.markdown("Visualiza y explora todos los datos utilizados en el proyecto. También puedes descargar la tabla como archivo Excel.")
    def formatear_dataframe(df):
        df_format = df.copy()
        for col in df_format.select_dtypes(include=["float", "int"]):
            df_format[col] = df_format[col].apply(formatear_numero)
        return df_format
    st.dataframe(formatear_dataframe(df), use_container_width=True, height=600)
    @st.cache_data
    def convertir_a_excel(df_original):
        import io
        from pandas import ExcelWriter
        output = io.BytesIO()
        with ExcelWriter(output, engine="openpyxl") as writer:
            df_original.to_excel(writer, index=False, sheet_name="Datos")
        return output.getvalue()
    archivo_excel = convertir_a_excel(df)
    st.download_button(
        label="📥 Descargar tabla como Excel",
        data=archivo_excel,
        file_name="tabla_de_datos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
