import streamlit as st

# 🔹 Configuración de la página
st.set_page_config(
    page_title="ScoutVision ⚽",
    page_icon="⚽",
    layout="wide"
)

# 🔹 Ocultar la barra lateral y menú de configuración de Streamlit si no está logueado
if "logueado" not in st.session_state:
    st.session_state.logueado = False
if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = None
if "mostrar_login" not in st.session_state:
    st.session_state.mostrar_login = False

if not st.session_state.logueado:
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            [data-testid="stSidebarNav"], [data-testid="stSidebar"], [data-testid="stToolbar"] {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)

# 🔹 Simulación de credenciales (usuario: contraseña)
USUARIOS_VALIDOS = {
    "admin": "1234",
     "admin": "admin",
    "usuario": "password"
}

# 🔹 Si el usuario NO está autenticado, mostrar la imagen y el formulario de login
if not st.session_state.logueado:
    # Mostrar imagen SOLO antes del login
    st.image("data/Captura de pantalla 2025-03-13 a las 9.00.27.png", clamp=True)

    # 🔹 Sección de bienvenida y presentación
    st.title("⚽ ScoutVision")
    st.markdown("""
        ## 📌 ¿Quiénes somos?
        Somos una plataforma de análisis deportivo que proporciona **herramientas avanzadas** para la evaluación del rendimiento de jugadores, comparación de estadísticas y toma de decisiones estratégicas.

        Nuestro objetivo es ayudar a **scouts** a optimizar su gestión deportiva con datos actualizados y visualizaciones interactivas.
                
        Con esta aplicación podrán tener un control de las puntuaciones de sus informes al mismo tiempo que manejarán la información necesaria sobre el rendimiento de los jugadores actuales.
    """)

    st.markdown("---")

    # 🔹 Formulario de contacto para solicitar acceso
    st.markdown("### 📩 ¿Te interesa acceder a la plataforma?")
    st.markdown("Si deseas recibir credenciales de acceso, por favor completa el siguiente formulario:")

    with st.form("contact_form"):
        nombre_contacto = st.text_input("✍ Nombre completo")
        correo_contacto = st.text_input("📧 Correo electrónico")
        mensaje_contacto = st.text_area("💬 Cuéntanos por qué te interesa nuestra plataforma")

        submit_contact = st.form_submit_button("📩 Enviar solicitud")

        if submit_contact:
            if nombre_contacto and correo_contacto and mensaje_contacto:
                st.success("✅ ¡Gracias por tu interés! Nos pondremos en contacto contigo pronto.")
            else:
                st.error("❌ Por favor, completa todos los campos antes de enviar.")

    st.markdown("---")

    # 🔹 Zona de Inicio de Sesión
    st.markdown("### 🔐 Acceso para Usuarios Registrados")

    if not st.session_state.mostrar_login:
        if st.button("🔑 Iniciar Sesión"):
            st.session_state.mostrar_login = True
            st.rerun()

    if st.session_state.get("mostrar_login", False):
        st.subheader("🔑 Iniciar Sesión")
        usuario = st.text_input("Usuario")
        contrasena = st.text_input("Contraseña", type="password")

        if st.button("Acceder"):
            if usuario in USUARIOS_VALIDOS and USUARIOS_VALIDOS[usuario] == contrasena:
                st.session_state.logueado = True
                st.session_state.usuario_actual = usuario
                st.success(f"✅ Bienvenido, {usuario}! Redirigiendo...")
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos.")

# 🔹 Si el usuario YA ESTÁ autenticado, mostrar la interfaz principal SIN la imagen
else:
    st.sidebar.success("🔍 Usa la barra lateral para navegar entre las secciones.")

    # 🔹 Botón para cerrar sesión
    if st.sidebar.button("Cerrar Sesión 🚪"):
        st.session_state.logueado = False
        st.session_state.usuario_actual = None
        st.rerun()

    # 🌟 Página de bienvenida después del login (SIN imagen)
    st.title(f"👋 ¡Bienvenido, {st.session_state.usuario_actual}!")
    st.markdown("""
        ### 🎉 Nos alegra verte de nuevo en el **Panel de Control de Jugadores**.
        Ahora puedes explorar las estadísticas y análisis disponibles en la plataforma.

        - 📊 **Consulta los datos más recientes** en la sección de análisis.
        - ⚽ **Compara el rendimiento de jugadores** en diferentes competiciones.
        - 🔍 **Obtén insights clave** para mejorar tu estrategia.

        👉 Usa la barra lateral de Streamlit para navegar entre las secciones.
    """)
    st.success("✅ ¡Todo está listo! Comienza explorando los datos.")







