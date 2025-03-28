import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import os

# 🔹 Configuración de la página
st.set_page_config(page_title="ScoutVision ⚽", page_icon="📊", layout="wide")

# 🔹 Verificar si el usuario está logueado
if "logueado" not in st.session_state or not st.session_state.logueado:
    st.warning("🔒 Debes iniciar sesión para acceder a esta página.")
    st.stop()
    

# 🔹 Función para cargar los datos
def cargar_datos():
    try:
        df = pd.read_excel("data/5grandesligas.xlsx", engine="openpyxl")
        df.columns = df.columns.str.strip()
        df["Minutos"] = df["Minutos"].astype(str).str.replace(",", "").astype(float)
        df["Edad"] = df["Edad"].astype(float)
        df["Gls/90"] = df["Gls/90"].astype(float)
        df["xG/90"] = df["xG/90"].astype(float)
        df["Disparos/90"] = df["Disparos/90"].astype(float)
        df["Regates_exito"] = df["Regates_exito"].astype(int)  # Convertir a entero (sin decimales)
        return df
    except Exception as e:
        st.error(f"Error cargando los datos: {e}")
        return pd.DataFrame()

df = cargar_datos()

# 🔹 Mostrar logo
logo_path = os.path.join("data", "fbrief-logo.webp")
if os.path.exists(logo_path):
    st.image(logo_path, clamp=True)

# 🔹 Filtros en la barra lateral
with st.sidebar:
    st.subheader("Filtros de Jugadores")
    competicion = st.selectbox("Selecciona Competición", ["TODAS"] + list(df["Competicion"].unique()))
    nombre_jugador = st.text_input("Buscar Jugador", placeholder="Nombre del jugador")
    nacionalidad = st.selectbox("Selecciona Nacionalidad", ["TODAS"] + list(df["Nacionalidad"].unique()))
    posicion = st.selectbox("Selecciona Posición", ["TODAS"] + list(df["Pos"].unique()))
    edad_range = st.slider("Rango de Edad", int(df["Edad"].min()), int(df["Edad"].max()), (int(df["Edad"].min()), int(df["Edad"].max())))
    minutos_range = st.slider("Rango de Minutos Jugados", int(df["Minutos"].min()), int(df["Minutos"].max()), (int(df["Minutos"].min()), int(df["Minutos"].max())))
    equipo = st.selectbox("Selecciona Equipo", ["TODOS"] + list(df["Equipo"].unique()))

# 🔹 Aplicar filtros
df_filtrado = df[(df["Jugador"].str.contains(nombre_jugador, case=False, na=False)) &
                 ((df["Competicion"] == competicion) | (competicion == "TODAS")) &
                 ((df["Nacionalidad"] == nacionalidad) | (nacionalidad == "TODAS")) &
                 ((df["Pos"] == posicion) | (posicion == "TODAS")) &
                 (df["Edad"] >= edad_range[0]) & (df["Edad"] <= edad_range[1]) &
                 (df["Minutos"] >= minutos_range[0]) & (df["Minutos"] <= minutos_range[1]) &
                 ((df["Equipo"] == equipo) | (equipo == "TODOS"))]

st.subheader("📊 Datos Filtrados")
st.dataframe(df_filtrado)

# 🔹 Gráficos
fig1 = px.scatter(df_filtrado, x="Gls/90", y="xG/90", color="Equipo", hover_data=["Jugador"], title="⚽ Eficacia Goleadora")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(df_filtrado.sort_values(by="Disparos/90", ascending=False).head(10), x="Jugador", y="Disparos/90", color="Equipo", title="🎯 Top 10 Disparos/90")
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.box(df_filtrado, x="Pos", y="Gls/90", color="Pos", title="📊 Distribución de Goles por Posición")
st.plotly_chart(fig3, use_container_width=True)

fig4 = px.scatter(df_filtrado, x="Edad", y="Minutos", color="Equipo", size="Gls/90", hover_data=["Jugador"], title="⏳ Relación entre Edad y Minutos Jugados")
st.plotly_chart(fig4, use_container_width=True)

fig5 = px.scatter(df_filtrado, x="Gls/90", y="Ast/90", color="Equipo", hover_data=["Jugador"], title="⚽ Goles vs Asistencias")
st.plotly_chart(fig5, use_container_width=True)


import os
import sqlite3
import pandas as pd
import streamlit as st

# 🔹 Base de datos SQLite para scouting
DB_FILE = "data/scouting.db"

def conectar_db():
    """Crea una base de datos de scouting sin columna ID."""
    if not os.path.exists("data"):
        os.makedirs("data")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Crear tabla de scouting sin ID
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scouting (
            jugador TEXT,
            partido TEXT,
            fecha TEXT,
            nota TEXT CHECK(nota IN ('A', 'B', 'C', 'D'))
        )
    ''')
    
    conn.commit()
    conn.close()

def cargar_scouting():
    conn = sqlite3.connect(DB_FILE)
    df_scouting = pd.read_sql("SELECT jugador, partido, fecha, nota FROM scouting", conn)
    conn.close()
    return df_scouting

# 🔹 Iniciar base de datos y cargar scouting
conectar_db()
df_scouting = cargar_scouting()

# 🔹 Mostrar datos de scouting
st.subheader("📄 Notas de Scouts")
if not df_scouting.empty:
    st.dataframe(df_scouting, use_container_width=True)
else:
    st.warning("⚠️ No hay datos disponibles en la base de datos.")

# 🔹 Función para actualizar el conteo de informes

def actualizar_conteo():
    global notas_recuento
    notas_recuento = df_scouting.pivot_table(index="jugador", columns="nota", aggfunc="size", fill_value=0).reset_index()
    notas_recuento.columns.name = None
    notas_recuento.rename(columns={"jugador": "Jugador", "A": "Informes A", "B": "Informes B", "C": "Informes C", "D": "Informes D"}, inplace=True)

# 🔹 Tabla de Conteo de Informes por Jugador
st.subheader("📊 Conteo de Informes por Jugador")
actualizar_conteo()
st.dataframe(notas_recuento, use_container_width=True)

# 🔹 Sección para subir un archivo Excel con nuevas notas de scouting
st.subheader("📥 Añadir Nuevo Informe de Scouting")
st.markdown("Sube un archivo Excel con los informes de scouting (mismas columnas que la base de datos).")

archivo_subido = st.file_uploader("Cargar archivo Excel", type=["xlsx"])
if archivo_subido:
    try:
        df_nuevo = pd.read_excel(archivo_subido, engine="openpyxl")
        columnas_requeridas = {"jugador", "partido", "fecha", "nota"}
        
        if not columnas_requeridas.issubset(df_nuevo.columns):
            st.error("❌ El archivo no tiene las columnas correctas. Asegúrate de que tenga: Jugador, Partido, Fecha, Nota.")
        else:
            conn = sqlite3.connect(DB_FILE)
            df_nuevo.to_sql("scouting", conn, if_exists="append", index=False)
            conn.close()
            
            st.success(f"✅ Se han añadido {len(df_nuevo)} nuevos informes a la base de datos.")
            
            # Recargar datos actualizados
            df_scouting = cargar_scouting()
            actualizar_conteo()
    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")
