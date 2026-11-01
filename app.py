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
    if st.button("🌟 Ejemplo 3.1: Equivalencia Local", use_container_width=True):
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
    st.subheader("Ejemplo 3.1: Equivalencia Local")
    
    pto_elegido = st.radio(
        "Seleccioná el punto de equilibrio a analizar:",
        ["Ensilladura en (0, -1)", "Sumidero en (0, 1)"],
        horizontal=True
    )
    
    radio = st.slider("Radio del entorno", 0.05, 3.0, 2.5, 0.05)
    
    if "Ensilladura" in pto_elegido:
        cx, cy = 0, -1
        U_l_func = lambda X, Y: -X
        V_l_func = lambda X, Y: 2 * (Y + 1)
        color_l = 'seagreen'
    else:
        cx, cy = 0, 1
        U_l_func = lambda X, Y: -X
        V_l_func = lambda X, Y: -2 * (Y - 1)
        color_l = 'darkorange'
        
    x = np.linspace(cx - radio, cx + radio, 400)
    y = np.linspace(cy - radio, cy + radio, 400)
    X, Y = np.meshgrid(x, y)
    
    U_nl, V_nl = -X, 1 - X**2 - Y**2
    U_l, V_l = U_l_func(X, Y), V_l_func(X, Y)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    ax1.streamplot(X, Y, U_nl, V_nl, density=1.2, color='royalblue')
    ax1.plot(0, -1, 'ko', markersize=8, label="Ensilladura (0,-1)")
    ax1.plot(0, 1, 'ro', markersize=8, label="Sumidero (0,1)")
    ax1.set_title("Sistema No Lineal")
    ax1.set_xlim(cx - radio, cx + radio)
    ax1.set_ylim(cy - radio, cy + radio)
    ax1.legend(loc='upper right')
    
    ax2.streamplot(X, Y, U_l, V_l, density=1.2, color=color_l)
    ax2.plot(cx, cy, 'ko' if cy == -1 else 'ro', markersize=8, label=f"Linealización en (0, {cy})")
    ax2.set_title(f"Linealización en (0, {cy})")
    ax2.set_xlim(cx - radio, cx + radio)
    ax2.set_ylim(cy - radio, cy + radio)
    ax2.legend(loc='upper right')
    
    st.pyplot(fig)

elif st.session_state.ejemplo_activo == '3.2':
    st.subheader("Ejemplo 3.2: Falla por Centro (Ausencia de Hiperbolicidad)")
    
    st.markdown("""
    **Sistema no lineal:**  
    $\dot{x} = -y - ax(x^2+y^2)^{1/2}$  
    $\dot{y} = x - ay(x^2+y^2)^{1/2}$  
    
    El análisis lineal arroja autovalores puramente imaginarios (centro). Sin embargo, variando el parámetro $a$, vemos que el comportamiento topológico real depende de los términos no lineales.
    """)
    
    a_val = st.slider("Parámetro 'a' (término no lineal)", min_value=-2.0, max_value=2.0, value=1.0, step=0.1)
    
    radio = 2.0
    x = np.linspace(-radio, radio, 400)
    y = np.linspace(-radio, radio, 400)
    X, Y = np.meshgrid(x, y)
    
    # Sistema no lineal
    R = np.sqrt(X**2 + Y**2)
    U_nl = -Y - a_val * X * R
    V_nl = X - a_val * Y * R
    
    # Sistema Linealizado en (0,0) siempre es un centro
    U_l = -Y
    V_l = X
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Gráfico No Lineal
    if a_val > 0:
        tipo = "Sumidero"
        color_nl = 'crimson'
    elif a_val < 0:
        tipo = "Fuente"
        color_nl = 'darkorange'
    else:
        tipo = "Centro"
        color_nl = 'gray'
        
    ax1.streamplot(X, Y, U_nl, V_nl, density=1.2, color=color_nl)
    ax1.plot(0, 0, 'ko', markersize=8, label="Equilibrio (0,0)")
    ax1.set_title(f"Sistema No Lineal (Realidad: {tipo})")
    ax1.set_xlim(-radio, radio)
    ax1.set_ylim(-radio, radio)
    ax1.legend(loc='upper right')
    
    # Gráfico Linealizado
    ax2.streamplot(X, Y, U_l, V_l, density=1.2, color='gray')
    ax2.plot(0, 0, 'ko', markersize=8, label="Equilibrio (0,0)")
    ax2.set_title("Linealización (Falso Positivo: Centro)")
    ax2.set_xlim(-radio, radio)
    ax2.set_ylim(-radio, radio)
    ax2.legend(loc='upper right')
    
    st.pyplot(fig)

elif st.session_state.ejemplo_activo == '3.3':
    st.subheader("Ejemplo 3.3: Punto Crítico Degenerado")
    st.info("Acá contrastaremos la linealización nula con el complejo retrato de fase del origen.")
