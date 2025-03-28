import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import os  

# 🔹 Configuración de la página
st.set_page_config(page_title="Análisis Transfermarkt", page_icon="⚽", layout="wide")

# 🔹 Aplicar CSS para que los gráficos se alineen con el tamaño del logo
st.markdown(
    """
    <style>
        .block-container {
            max-width: 95%;
            margin: auto;
        }
        .stPlotlyChart {
            margin-left: auto;
            margin-right: auto;
        }
        .logo-container {
            display: flex;
            justify-content: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 🔹 Verificar si el usuario está logueado
if "logueado" not in st.session_state or not st.session_state.logueado:
    st.warning("🔒 Debes iniciar sesión para acceder a esta página.")
    st.stop()

# 🔹 Cargar el archivo Excel
file_path = os.path.join("data", "Transfermark.xlsx")

if os.path.exists(file_path):
    df = pd.read_excel(file_path, sheet_name="Sheet1")
else:
    st.error("❌ No se encontró el archivo de datos. Verifica la ruta.")
    st.stop()

# 🔹 Mostrar logo SIN cambiar su tamaño, alineando los gráficos con él
logo_path = os.path.join("data", "Transfermarkt_logo.png")

if os.path.exists(logo_path):
    st.image(logo_path, clamp=True)  # Mantiene el tamaño original

# 🔹 Título principal
st.markdown("<h1 style='text-align: center; color: #1E90FF;'>📊 Análisis de Datos de Transfermarkt</h1>", unsafe_allow_html=True)

# 🔹 Sidebar con filtros personalizados
st.sidebar.header("🔍 Filtros de Búsqueda")
jugador_busqueda = st.sidebar.text_input("🔎 Buscar jugador (nombre exacto o parcial)")

edad_min, edad_max = st.sidebar.slider("Edad", int(df["Edad"].min()), int(df["Edad"].max()), 
    (int(df["Edad"].min()), int(df["Edad"].max())))

valor_min, valor_max = st.sidebar.slider("Valor de Mercado (€ Millones)", 
    float(df["Valor Mercado"].min()), float(df["Valor Mercado"].max()), 
    (float(df["Valor Mercado"].min()), float(df["Valor Mercado"].max())))

posiciones_opciones = ["Todas"] + list(df["Pos"].unique())
posicion = st.sidebar.multiselect("📌 Posición", posiciones_opciones, ["Todas"])

competicion_opciones = ["Todas"] + list(df["Competicion"].unique())
competicion = st.sidebar.multiselect("🏆 Competición", competicion_opciones, ["Todas"])

# 🔹 Aplicar filtros
posicion_filtrada = df["Pos"].unique().tolist() if "Todas" in posicion else posicion
competicion_filtrada = df["Competicion"].unique().tolist() if "Todas" in competicion else competicion

filtered_df = df[
    (df["Edad"] >= edad_min) & (df["Edad"] <= edad_max) &
    (df["Valor Mercado"] >= valor_min) & (df["Valor Mercado"] <= valor_max) &
    (df["Pos"].isin(posicion_filtrada)) &
    (df["Competicion"].isin(competicion_filtrada))
]

if jugador_busqueda:
    filtered_df = filtered_df[filtered_df["Jugador"].str.contains(jugador_busqueda, case=False, na=False)]

# 🔹 Mostrar la base de datos filtrada
st.markdown("### 📋 Datos de jugadores filtrados")
st.dataframe(filtered_df, use_container_width=True)

# 🔹 Colores personalizados para gráficos
color_palette = px.colors.qualitative.Safe  

# 📊 Gráficos (MISMO ORDEN, AJUSTADOS AL TAMAÑO DEL LOGO)
st.markdown("### 📈 Análisis Visual")

# 📊 Distribución de edades
st.markdown("### 📈 Distribución de edades de los jugadores")
fig_age = px.histogram(filtered_df, x="Edad", nbins=10, color_discrete_sequence=[color_palette[0]])
st.plotly_chart(fig_age, use_container_width=True)

# 📊 Valor de mercado promedio por posición
st.markdown("### 💰 Valor de mercado promedio por posición")
fig_market = px.bar(
    filtered_df.groupby("Pos")["Valor Mercado"].mean().reset_index(),
    x="Pos", y="Valor Mercado", color="Pos", color_discrete_sequence=color_palette
)
st.plotly_chart(fig_market, use_container_width=True)

# 📊 Cantidad de jugadores por posición
st.markdown("### ⚽ Cantidad de jugadores por posición")
pos_count_df = filtered_df["Pos"].value_counts().reset_index(name="count").rename(columns={"index": "Pos"})
fig_count = px.bar(pos_count_df, x="Pos", y="count", color="Pos", color_discrete_sequence=color_palette)
st.plotly_chart(fig_count, use_container_width=True)

# 📊 Valor total de mercado por competición
st.markdown("### 🏆 Valor total de mercado por competición")
fig_comp = px.bar(
    filtered_df.groupby("Competicion")["Valor Mercado"].sum().reset_index().sort_values("Valor Mercado", ascending=False),
    x="Competicion", y="Valor Mercado", color="Competicion", color_discrete_sequence=color_palette
)
st.plotly_chart(fig_comp, use_container_width=True)

# 📊 Relación entre Edad y Valor de Mercado
st.markdown("### 🔍 Relación entre Edad y Valor de Mercado")
fig_scatter = px.scatter(
    filtered_df, x="Edad", y="Valor Mercado", color="Competicion",
    hover_data=["Jugador", "Competicion"], color_discrete_sequence=color_palette
)
st.plotly_chart(fig_scatter, use_container_width=True)

# 📊 Jugadores/Valor de Mercado
st.markdown("### 🔍 Jugadores/Valor de Mercado")
fig_scatter2 = px.scatter(
    filtered_df, x="Jugador", y="Valor Mercado", color="Competicion",
    hover_data=["Jugador", "Competicion"], color_discrete_sequence=color_palette
)
st.plotly_chart(fig_scatter2, use_container_width=True)




















