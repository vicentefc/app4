import streamlit as st
import pandas as pd
import requests
import plotly.express as px

def obtener_terremotos(rango_inicio, rango_fin, min_magnitud):
    try:
        url = f"https://earthquake.usgs.gov/fdsnws/event/1/query"
        params = {
            "format": "geojson",
            "starttime": rango_inicio,
            "endtime": rango_fin,
            "minmagnitude": min_magnitud
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        datos = response.json()["features"]
        terremotos = []
        for evento in datos:
            propiedades = evento["properties"]
            coordenadas = evento["geometry"]["coordinates"]
            terremotos.append({
                "Magnitud": propiedades.get("mag"),
                "Lugar": propiedades.get("place"),
                "Fecha": pd.to_datetime(propiedades.get("time"), unit="ms"),
                "Longitud": coordenadas[0],
                "Latitud": coordenadas[1],
                "Profundidad (km)": coordenadas[2],
            })
        return pd.DataFrame(terremotos)
    except Exception as e:
        st.error(f"Error al obtener datos: {e}")
        return pd.DataFrame()

st.title("Actividad Sísmica Global")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    rango_inicio = st.date_input("Fecha de inicio", value=pd.Timestamp("2023-01-01"))
    rango_fin = st.date_input("Fecha de fin", value=pd.Timestamp("2023-12-31"))
    min_magnitud = st.slider("Magnitud mínima", min_value=0.0, max_value=10.0, value=4.0, step=0.1)

if st.button("Obtener datos"):
    df = obtener_terremotos(rango_inicio, rango_fin, min_magnitud)
    if not df.empty:
        st.success(f"Se encontraron {len(df)} terremotos.")
        fig = px.scatter_mapbox(
            df,
            lat="Latitud",
            lon="Longitud",
            size="Magnitud",
            hover_data=["Lugar", "Fecha", "Profundidad (km)"],
            mapbox_style="open-street-map",  # Garantiza compatibilidad universal del mapa
            title="Mapa de Actividad Sísmica",
            zoom=1,
        )
        fig.update_traces(marker=dict(color="red", opacity=0.6))  # Círculos rojos
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No se encontraron terremotos en el rango seleccionado.")
