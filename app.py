import requests
import pandas as pd
import streamlit as st
import plotly.express as px

def get_crypto_data(cryptos, currencies):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(cryptos)}&vs_currencies={','.join(currencies)}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {}

def process_data(data):
    processed = []
    for crypto, values in data.items():
        for currency, price in values.items():
            processed.append({"Crypto": crypto, "Currency": currency, "Price": price})
    return pd.DataFrame(processed)

def main():
    st.set_page_config(page_title="Dashboard de Criptomonedas", layout="wide")
    st.title("💰 Dashboard de Criptomonedas")

    st.sidebar.header("Configuraciones")

    if st.sidebar.button("Seleccionar criptomonedas comunes"):
        default_cryptos = "bitcoin,ethereum,cardano,solana"
    else:
        default_cryptos = "bitcoin,ethereum"
    
    if st.sidebar.button("Seleccionar monedas fiat comunes"):
        default_currencies = "usd,eur,gbp"
    else:
        default_currencies = "usd,eur"

    cryptos = st.sidebar.text_area("ids de criptomonedas (separadas por coma)", value=default_cryptos)
    currencies = st.sidebar.text_area("Monedas fiat (separadas por coma)", value=default_currencies)

    crypto_list = cryptos.split(",")
    currency_list = currencies.split(",")

    if st.sidebar.button("Obtener datos"):
        data = get_crypto_data(crypto_list, currency_list)
        if data:
            df = process_data(data)

            st.subheader("📊 Datos procesados")
            st.dataframe(df, use_container_width=True)
            st.divider()

            st.subheader("📈 Estadísticas descriptivas")
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Número de datos:** {len(df)}")
                avg_prices = df.groupby("Crypto")["Price"].mean().reset_index()
                fig_avg = px.bar(
                    avg_prices,
                    x="Crypto",
                    y="Price",
                    title="Promedio de precios por criptomoneda",
                    color_discrete_sequence=["red"]
                )
                st.plotly_chart(fig_avg, use_container_width=True)

            with col2:
                fig_dist = px.box(
                    df,
                    x="Crypto",
                    y="Price",
                    title="Distribución de precios por criptomoneda",
                    color_discrete_sequence=["red"]
                )
                st.plotly_chart(fig_dist, use_container_width=True)

            st.divider()

            st.subheader("📉 Comparación de precios")
            fig_comp = px.bar(
                df,
                x="Crypto",
                y="Price",
                color="Currency",
                title="Precios por criptomoneda y moneda fiat",
                color_discrete_sequence=["red"]
            )
            st.plotly_chart(fig_comp, use_container_width=True)

        else:
            st.error("Error al obtener datos de la API")
    
if __name__ == "__main__":
    main()
