import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Cars Analysis", page_icon="icon.png")

st.title('Análisis de autos nuevos y usados')
st.header("By sag")
st.markdown("""Axel Gustavo Peña Sánchez - S20006742\n
zS20006742@estudiantes.uv.mx""")

DATA_URL = ('cars_data.csv')

@st.cache_resource
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    return data
data = load_data(15000)

# Sidebar
st.sidebar.image("logo.png")

if st.sidebar.checkbox('Mostrar todos los datos'):
    st.subheader('Dataset')
    st.write(data)

query = st.sidebar.text_input("Buscar marca: ")
query = query.upper()
if st.sidebar.button('Buscar', key='button1'):
    results = data[data["make"].str.upper().str.contains(query)]
    st.header('Marcas encontradas:')
    st.write(results)

query = st.sidebar.text_input("Buscar modelo: ")
query = query.upper()
if st.sidebar.button('Buscar', key='button2'):
    data['model'] = data['model'].dropna()
    data['model'] = data['model'].astype(str)
    results = data[data["model"].str.upper().str.contains(query)]
    st.header('Modelos encontrados:')
    st.write(results)

# Multiselect
st.sidebar.markdown("##")
gear = st.sidebar.multiselect("Selecciona el tipo de transmisión",
                              data["gear"].unique(), default=data["gear"].unique())
gearFilter = data[data["gear"].isin(gear)]
if st.sidebar.checkbox('Mostrar datos', key="buttonS2"):
    st.subheader('Transmisión')
    st.write(gearFilter)

st.sidebar.markdown("##")
offerType = st.sidebar.multiselect(
    "Selecciona el estado del auto", data["offerType"].unique(), default=data["offerType"].unique())
offerTypeFilter = data[data["offerType"].isin(offerType)]
if st.sidebar.checkbox('Mostrar datos', key="buttonS3"):
    st.subheader('Estado')
    st.write(offerTypeFilter)

st.sidebar.markdown("##")
fuel = st.sidebar.multiselect("Selecciona el tipo de combustible",
                              data["fuel"].unique(), default=data["fuel"].unique())
fuelFilter = data[data["fuel"].isin(fuel)]
if st.sidebar.checkbox('Mostrar datos', key="buttonS4"):
    st.subheader('Combustible')
    st.write(fuelFilter)

# Histogram
fig, ax = plt.subplots()
ax.hist(data['year'], bins=15)
ax.set_xlabel('Año')
ax.set_ylabel('Cantidad')
ax.set_title('Modelos')
plt.style.use('dark_background')
st.sidebar.markdown("##")
if st.sidebar.checkbox('Mostrar histograma', key="buttonHistogram"):
    st.pyplot(fig)
    st.markdown(
        'Este histograma muestra la cantidad de autos de diferentes años')

# Barsgraph
selection = data.query(
    "gear == @gear & offerType == @offerType & fuel == @fuel")
fig = px.bar(selection, x="price", y=["gear", "offerType"])
fig.update_xaxes(title='Categorías')
fig.update_yaxes(title='Valores')
if st.sidebar.checkbox('Mostrar gráfica de barras', key="buttonBarsGraph"):
    st.plotly_chart(fig)
    st.markdown(
        'Esta gráfica de barras muestra la cantidad de autos según su condición y transmisión')

# Scattergraph
avgPricecars = selection['price']
fig = px.scatter(selection,
                 x=selection["price"].index,
                 y=avgPricecars,
                 template="plotly_white")
fig.update_xaxes(title='Autos')
fig.update_yaxes(title='Precio')
fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
if st.sidebar.checkbox('Mostrar gráfica scatter', key="buttonScatterGraph"):
    st.plotly_chart(fig)
    st.markdown(
        'Esta gráfica de dispersión muestra los precios de todos los autos')
