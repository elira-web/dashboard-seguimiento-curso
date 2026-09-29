import streamlit as st
import pandas as pd
import io

# 1. Configuración de la página
st.set_page_config(page_title="Seguimiento de Curso ETM", layout="wide", page_icon="📊")

st.title("📊 Panel de Seguimiento - Responsables Regionales")
st.markdown("Seleccione su departamento para visualizar y descargar el avance de los participantes (Exclusivo ETM).")

# 2. Función para cargar y transformar los datos
@st.cache_data
def load_data():
    # Leer el archivo original
    df = pd.read_excel("Reporte Lin 2da ED.xlsx")
    
    # Mapeo de columnas solicitadas
    columnas_req = {
        'Número de documento': 'DNI',
        'Dirección de correo': 'Correo',
        'Nombre': 'Nombre',
        'Apellido': 'Apellido',
        'Sexo': 'Sexo',
        'Perfil': 'Nivel de gobierno',
        'Institución': 'Institución',
        'Cargo': 'Cargo',
        'Es_ETM': 'Es ETM',
        'Departamento_ETM': 'Departamento ETM',
        'Provincia_ETM': 'Provincia ETM',
        'Distrito_ETM': 'Distrito ETM',
        'Avance del último ítem realizado': 'Avance del último ítem realizado',
        'Promedio': 'Promedio',
        'Estado del Promedio': 'Estado del Promedio'
    }
    
    # Filtrar solo las columnas mapeadas y renombrarlas
    df = df[list(columnas_req.keys())].rename(columns=columnas_req)
    
    # Filtro principal: Excluir los "No" en Es ETM
    df = df[df['Es ETM'] != 'No']
    
    # Asegurar que el DNI se vea como texto y no como número con decimales
    df['DNI'] = df['DNI'].astype(str)
    df['Es ETM'] = df['Es ETM'].astype(str)
    
    return df

# Cargar los datos
df_clean = load_data()

# 3. Interfaz del Dashboard (Filtros)
departamentos = ['Todos'] + sorted(df_clean['Departamento ETM'].dropna().unique().tolist())
dep_seleccionado = st.selectbox("📍 Seleccione un Departamento:", departamentos)

# Aplicar el filtro según selección
if dep_seleccionado == 'Todos':
    df_filtrado = df_clean
else:
    df_filtrado = df_clean[df_clean['Departamento ETM'] == dep_seleccionado]

# 4. Mostrar los datos en pantalla
st.write(f"### Visualizando registros: {len(df_filtrado)}")
st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

# 5. Lógica de Descarga Directa en Excel (.xlsx)
# Creamos un buffer en memoria para no guardar archivos temporales
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
    df_filtrado.to_excel(writer, index=False, sheet_name='Reporte ETM')

# Crear el botón de descarga
st.download_button(
    label=f"📥 Descargar Base de Datos (.xlsx) - {dep_seleccionado}",
    data=buffer.getvalue(),
    file_name=f"Reporte_ETM_{dep_seleccionado}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    type="primary"
)
