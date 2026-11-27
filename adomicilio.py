# La app de mi proyecto
# Para verla, en la terminal: streamlit run app.py
# Son los mismos pasos que en app_pisos.py y app_titanic.py. Si te atascas, busca el mismo paso allí.



# Paso 1. La página
# 1.1 Importa streamlit y pandas.

import streamlit as st # para la página
import pandas as pd  # para las tablas
import plotly.express as px

# 1.2 Pon el nombre de la pestaña del navegador, la página a todo lo ancho y un título que diga de qué va tu proyecto.

st.set_page_config(page_title="La Consulta",page_icon="🍲",layout="wide") # el nombre de la pestaña, el icono y la página a todo lo ancho
st.title("Bar La Consulta") # el título de la página

# 1.3 Debajo, una o dos frases con st.write: qué pregunta responde la app y de dónde salen los datos.

st.markdown("### ¿Con qué plataforma te quedas? ¿Qué plato prefieres y a qué barrio te lo llevamos?")
st.write("¡Tu consulta al gusto!")
st.write("Datos obtenidos del registro de pedidos a domicilio y la carta del restaurante.")


# Paso 2. Los datos
# 2.1 La función cargar_datos, con @st.cache_data encima, que lea "datos/datos_limpios.csv" y lo devuelva.
#     La limpieza ya está hecha en el cuaderno, así que la función solo lee y devuelve, como en la carta del bar.

@st.cache_data # lee y limpia el CSV una sola vez, no en cada clic
def cargar_datos():
    pedidos = pd.read_csv("pedidos_limpios.csv")
    platos = pd.read_csv("platos.csv")
    return pedidos, platos

# 2.2 Llama a la función y guarda la tabla en una variable con el nombre de tus datos.

pedidos, platos = cargar_datos()
st.write("Tenemos",len(pedidos), "pedidos y ",len(platos), "platos")

# Paso 3. Los filtros
# 3.1 En la barra de la izquierda (with st.sidebar:), al menos dos filtros:
#     un desplegable o unos botones para una columna de texto, con "Todos" al principio,
#     y una barra para una columna de números.

with st.sidebar: #todo lo que pongamos aquí va en la barra de la izquierda
    st.header("Filtros") #un título para los filtros
    plataformas= sorted(pedidos["plataforma"].unique()) #las plataformas ordenadas alfabéticamente
    plataformas.insert(0, "Todas") #Añadimos la opción de todas
    plataforma=st.selectbox("Plataforma", plataformas) #el desplegable de las plataformas
    total_min, total_max = st.slider("Precio pedido", 2.0, 90.0, (2.0, 90.0)) # el total en un slider de dos puntas


# Paso 4. Filtrar
# 4.1 Empieza con filtrados = tu tabla, y después aplica un filtro por cada widget, como en los pisos.
filtrados= pedidos #empezamos con todas los pedidos y vamos filtrando

if plataforma != "Todas":  # si se ha elegido una plataforma en concreto
    filtrados= filtrados[filtrados["plataforma"]==plataforma]   #nos quedamos con pedidos de esas plataformas
filtrados=filtrados[(filtrados["total"]>= total_min)] #nos quedamos con los pedidos que estén en esos precios
filtrados=filtrados[(filtrados["total"]<= total_max)] #nos quedamos con los pedidos que estén en esos precios

# Paso 5. Si no queda nada
# 5.1 Si filtrados está vacía, saca un aviso con st.warning y para el programa con st.stop().

if len(filtrados)==0: # si no hay ningún país que cumpla los filtros
    st.warning("No hay ningún pedido que cumpla los filtros seleccionados.")  #aviso
    st.stop() #y paramos la ejecución para que no de error al calcular las métricas


# Paso 6. Las métricas
# 6.1 Cuatro métricas en columnas, con los números más importantes para tu consulta.

col1, col2, col3, col4 = st.columns(4)  # cuatro columnas para las métricas

num_pedidos = len(filtrados)  # cuántos pedidos encajan con los filtros actuales
with col1:
    st.metric("Total pedidos", num_pedidos)

with col2:
    facturacion = round(filtrados["total"].sum(), 2) if num_pedidos > 0 else 0.0
    st.metric("Facturación total (€)", facturacion)

with col3:
    ticket_medio = round(filtrados["total"].mean(), 2) if num_pedidos > 0 else 0.0
    st.metric("Ticket medio (€)", ticket_medio)

with col4:
    tiempo_medio = round(filtrados["minutos"].mean(), 1) if num_pedidos > 0 else 0.0
    st.metric("Tiempo espera medio (min)", tiempo_medio)

# Paso 7. Las pestañas
tab1, tab2, tab3 = st.tabs(["Pedidos filtrados", "Canales y tiempos", "¿Qué pasaría si...?"])

with tab1:
    st.header("Pedidos filtrados")
    if not filtrados.empty:
        st.dataframe(filtrados, use_container_width=True)
    else:
        st.warning("No hay pedidos con estos filtros.")

with tab2:
    st.header("Rendimiento por plataforma")
    if not filtrados.empty:
        c1, c2 = st.columns(2)

        with c1:
            por_plat = filtrados.groupby("plataforma", as_index=False)["total"].sum()
            fig_plat = px.bar(por_plat, x="plataforma", y="total", title="Facturación por plataforma")
            st.plotly_chart(fig_plat, use_container_width=True)

        with c2:
            fig_hist = px.histogram(filtrados, x="total", nbins=15, title="Distribución de importes (€)")
            st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.info("Ajusta los filtros de la barra lateral para ver los gráficos.")

with tab3:
    st.header("Simulador rápido de ticket")
    umbral = st.slider("Ver pedidos con importe igual o mayor a (€):", 2.0, 90.0, 20.0, key="sim_umbral")
    subset_sim = filtrados[filtrados["total"] >= umbral]
    num_sim = len(subset_sim)
    total_sim = 0.0 if num_sim == 0 else round(subset_sim["total"].sum(), 2)
    st.write("Con el filtro actual,", num_sim, "pedidos superan o igualan los", umbral, "€, sumando", total_sim, "€.")