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
st.write("Esta aplicación muestra los datos de la tabla `Super_DanielSM` alojada en SQL Server.")

# Función para obtener la conexión a SQL Server
@st.cache_resource
def init_connection():
    # Detectar automáticamente qué driver está disponible
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
        raise Exception(f"No se encontró un driver ODBC de SQL Server. Disponibles: {drivers_disponibles}")

    conn_str = (
        f"DRIVER={{{driver_seleccionado}}};"
        f"SERVER={st.secrets['server']};"
        f"DATABASE={st.secrets['database']};"
        f"UID={st.secrets['username']};"
        f"PWD={st.secrets['password']};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=yes;"
        f"Connection Timeout=30;"
    )
    return pyodbc.connect(conn_str)

# Función para cargar los datos de la tabla
def load_data():
    conn = init_connection()
    query = "SELECT * FROM dbo.Super_DanielSM ORDER BY ID DESC"
    df = pd.read_sql(query, conn)
    return df

# --- Lógica principal de la App ---
try:
    df = load_data()

    if df.empty:
        st.warning("La tabla está vacía. No hay datos para mostrar.")
    else:
        st.success(f"✅ Se cargaron {len(df)} registros correctamente.")
        st.dataframe(df, use_container_width=True, hide_index=True)

        with st.expander("ℹ️ Ver información de las columnas"):
            st.write("**Columnas disponibles:**")
            st.write(list(df.columns))

except Exception as e:
    st.error("❌ Error al conectar con la base de datos.")
    st.error(f"Detalles técnicos: {e}")
    st.info("Verifica las credenciales en Secrets y que el servidor de Somee permita conexiones externas.")