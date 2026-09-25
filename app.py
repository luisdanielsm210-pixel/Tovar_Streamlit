import streamlit as st
import pandas as pd
import pyodbc

# Configuración de la página
st.set_page_config(
    page_title="Datos Super DanielSM",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Registros de Super_DanielSM")
st.write("Aplicación conectada a SQL Server (Somee).")

# ---------- Conexión ----------
@st.cache_resource
def init_connection():
    drivers_disponibles = [d for d in pyodbc.drivers()]
    driver_seleccionado = None
    for posible in [
        "ODBC Driver 18 for SQL Server",
        "ODBC Driver 17 for SQL Server",
        "SQL Server"
    ]:
        if posible in drivers_disponibles:
            driver_seleccionado = posible
            break

    if not driver_seleccionado:
        raise Exception(f"No se encontró driver ODBC. Disponibles: {drivers_disponibles}")

    conn_str = (
        f"DRIVER={{{driver_seleccionado}}};"
        f"SERVER={st.secrets['server']};"
        f"DATABASE={st.secrets['database']};"
        f"UID={st.secrets['username']};"
        f"PWD={st.secrets['password']};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=yes;"
        f"Connection Timeout=30;"
        f"MARS_Connection=yes;"
    )
    return pyodbc.connect(conn_str)

# ---------- Cargar datos ----------
def load_data():
    conn = init_connection()
    query = "SELECT * FROM dbo.Super_DanielSM ORDER BY ID DESC"
    return pd.read_sql(query, conn)

# ---------- Insertar registro ----------
def insertar_registro(nombre, fecha, hora):
    conn = init_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO dbo.Super_DanielSM (Nombre, Fecha, Hora) VALUES (?, ?, ?)",
        (nombre, fecha, hora)
    )
    conn.commit()
    cursor.close()

# ---------- Interfaz ----------
tab1, tab2 = st.tabs(["📋 Ver registros", "➕ Agregar registro"])

with tab1:
    try:
        df = load_data()
        if df.empty:
            st.warning("La tabla está vacía. Ve a la pestaña 'Agregar registro' para insertar datos.")
        else:
            st.success(f"✅ Se cargaron {len(df)} registros.")
            st.dataframe(df, use_container_width=True, hide_index=True)
            with st.expander("ℹ️ Columnas"):
                st.write(list(df.columns))
    except Exception as e:
        st.error(f"❌ Error al consultar: {e}")

with tab2:
    st.subheader("Agregar nuevo registro")
    with st.form("form_insertar"):
        nombre = st.text_input("Nombre")
        fecha = st.date_input("Fecha")
        hora = st.time_input("Hora")
        enviado = st.form_submit_button("Guardar")

        if enviado:
            if not nombre.strip():
                st.error("El nombre no puede estar vacío.")
            else:
                try:
                    insertar_registro(nombre, fecha, hora)
                    st.success(f"✅ Registro guardado: {nombre}")
                    st.cache_resource.clear()  # refrescar datos
                except Exception as e:
                    st.error(f"❌ Error al guardar: {e}")