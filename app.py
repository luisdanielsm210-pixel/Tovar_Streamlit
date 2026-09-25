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
    conn_str = f"""
    DRIVER={{ODBC Driver 18 for SQL Server}};
    SERVER={st.secrets["server"]};
    DATABASE={st.secrets["database"]};
    UID={st.secrets["username"]};
    PWD={st.secrets["password"]};
    Encrypt=yes;
    TrustServerCertificate=yes;
    Connection Timeout=30;
    """
    return pyodbc.connect(conn_str)

# Función para cargar los datos de la tabla
def load_data():
    conn = init_connection()
    query = "SELECT * FROM dbo.Super_DanielSM"
    df = pd.read_sql(query, conn)
    return df

# --- Lógica principal de la App ---
try:
    # Cargar los datos
    df = load_data()
    
    if df.empty:
        st.warning("La tabla está vacía. No hay datos para mostrar.")
    else:
        st.success(f"✅ Se cargaron {len(df)} registros correctamente.")
        
        # Mostrar los datos en una tabla interactiva
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
        
        # Mostrar un pequeño resumen
        with st.expander("ℹ️ Ver información de las columnas"):
            st.write("**Columnas disponibles:**")
            st.write(list(df.columns))
            
except Exception as e:
    st.error("❌ Error al conectar con la base de datos.")
    st.error(f"Detalles técnicos: {e}")
    st.info("Verifica que las credenciales en `secrets.toml` sean correctas y que el servidor de Somee esté activo.")