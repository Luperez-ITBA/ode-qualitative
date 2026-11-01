import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Grobman-Hartman Explorer", layout="wide")

# 1. Inicializar la variable de estado para la navegación
if 'ejemplo_activo' not in st.session_state:
    st.session_state.ejemplo_activo = '3.1'

st.title("Estudio Cualitativo de ODEs: Teorema de Grobman-Hartman")

# 2. Crear el menú visible tipo "íconos" con botones anchos
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🌟 Ejemplo 3.1: Ensilladura (Éxito)", use_container_width=True):
        st.session_state.ejemplo_activo = '3.1'
with col2:
    if st.button("🌀 Ejemplo 3.2: Falla por Centro", use_container_width=True):
        st.session_state.ejemplo_activo = '3.2'
with col3:
    if st.button("⚠️ Ejemplo 3.3: Punto Degenerado", use_container_width=True):
        st.session_state.ejemplo_activo = '3.3'

st.markdown("---")

# 3. Mostrar el contenido dependiendo del botón activo
if st.session_state.ejemplo_activo == '3.1':
    st.subheader("Ejemplo 3.1: Equivalencia Local (Ensilladura)")
    
    radio = st.slider("Radio del entorno centrado en (0, -1)", 0.05, 3.0, 2.5, 0.05)
    
    x = np.linspace(-radio, radio, 400)
    y = np.linspace(-1 - radio, -1 + radio, 400)
    X, Y = np.meshgrid(x, y)
    
    U_nl, V_nl = -X, 1 - X**2 - Y**2
    U_l, V_l = -X, 2 * (Y + 1)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    ax1.streamplot(X, Y, U_nl, V_nl, density=1.2, color='royalblue')
    ax1.plot(0, -1, 'ko', markersize=8)
    if radio >= 2.0:
        ax1.plot(0, 1, 'ro', markersize=8)
    ax1.set_title("Sistema No Lineal")
    
    ax2.streamplot(X, Y, U_l, V_l, density=1.2, color='seagreen')
    ax2.plot(0, -1, 'ko', markersize=8)
    ax2.set_title("Linealización en (0, -1)")
    
    st.pyplot(fig)

elif st.session_state.ejemplo_activo == '3.2':
    st.subheader("Ejemplo 3.2: Ruptura de Equivalencia Topológica")
    st.info("Acá irá la simulación donde variamos el parámetro 'a' para destruir el centro.")

elif st.session_state.ejemplo_activo == '3.3':
    st.subheader("Ejemplo 3.3: Punto Crítico Degenerado")
    st.info("Acá contrastaremos la linealización nula con el complejo retrato de fase del origen.")
