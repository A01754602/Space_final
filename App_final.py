import streamlit as st
import numpy as np
import requests

# Establecer título y estilo de la página
st.set_page_config(page_title="Spaceship Titanic - Supervivencia", page_icon="🚀")

# CSS para darle estilo espacial
page_bg_img = """
<style>
body {
    background-image: url("https://www.nasa.gov/sites/default/files/thumbnails/image/stsci-h-p2041a-f-3840x2160.png");
    background-size: cover;
    color: white;
}
h1, h2, h3 {
    color: #00FF00;
}
.stButton>button {
    background-color: #00FF00;
    color: black;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Título con diseño temático
st.title("🪐 Predicción de Supervivencia en el Titanic Espacial 🛸")

# Subtítulo con un breve texto
st.subheader("🚀 ¿Sobrevivirías el viaje interestelar? Descúbrelo con nuestro modelo de predicción 🤖")

# Crear selectboxes y radio buttons para todas las entradas categóricas y numéricas
home_planet = st.selectbox("🌍 Planeta de origen", ["Earth", "Europa", "Mars"])

cryosleep = st.radio("❄️ ¿Estaba en Criosueño?", ["Sí", "No"])

destination = st.selectbox("🌌 Destino", ["TRAPPIST-1e", "55 Cancri e", "PSO J318.5-22"])

deck = st.selectbox("🛳️ Deck", ["A", "B", "C", "D", "E", "F", "G", "T"])

side = st.radio("🔄 Lado de la cabina", ["P", "S"])

vip = st.radio("💎 ¿Es VIP?", ["Sí", "No"])

# Crear selectboxes para valores numéricos, puedes también usar sliders si prefieres.
age = st.selectbox("👶 Edad", list(range(0, 101)))  # Lista de 0 a 100
room_service = st.selectbox("🛎️ Room Service", list(range(0, 10001, 100)))  # Incrementos de 100
food_court = st.selectbox("🍔 Food Court", list(range(0, 10001, 100)))
shopping_mall = st.selectbox("🛒 Shopping Mall", list(range(0, 10001, 100)))
spa = st.selectbox("🛀 Spa", list(range(0, 10001, 100)))
vr_deck = st.selectbox("🎮 VR Deck", list(range(0, 10001, 100)))
num = st.selectbox("🔢 Número de Cabina", list(range(0, 2001)))  # De 0 a 2000

# Botón para predecir con efecto hover
if st.button("🌟 Predecir Supervivencia"):
    # Convertir las entradas a los valores correctos que el modelo espera
    cryosleep_val = 1 if cryosleep == "Sí" else 0
    vip_val = 1 if vip == "Sí" else 0
    home_planet_val = {"Earth": 0.424, "Europa": 0.626, "Mars": 0.5586}[home_planet]
    destination_val = {"TRAPPIST-1e": 0.4711, "55 Cancri e": 0.61, "PSO J318.5-22": 0.5037}[destination]
    deck_val = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "T": 7}[deck]
    side_val = {"P": 0, "S": 1}[side]

    # Crear el JSON con los datos
    input_data = {
        "HomePlanet": home_planet_val,
        "CryoSleep": cryosleep_val,
        "Destination": destination_val,
        "Age": age,
        "VIP": vip_val,
        "RoomService": room_service,
        "FoodCourt": food_court,
        "ShoppingMall": shopping_mall,
        "Spa": spa,
        "VRDeck": vr_deck,
        "Deck": deck_val,
        "Num": num,
        "Side": side_val
    }

    # Llamada a la API (recuerda ajustar la URL a la correcta)
    FLASK_API_URL = "http://54.91.148.212:8080/predictjson"  # Cambia la IP si es necesario

    try:
        response = requests.post(FLASK_API_URL, json=input_data)
        response.raise_for_status()  # Verifica que no hubo un error HTTP
        prediction = response.json().get('Prediction')

        # Mostrar el resultado de la predicción
        if prediction:
            st.success('🟢 ¡El pasajero sobrevivirá la aventura espacial! 🎉')
        else:
            st.error('🔴 Desafortunadamente, el pasajero no sobrevivirá. 💫')

    except requests.exceptions.HTTPError as http_err:
        st.error(f"Error HTTP: {http_err}")
    except requests.exceptions.RequestException as err:
        st.error(f"Error: {err}")
    except ValueError as json_err:
        st.error(f"Error al procesar la respuesta JSON: {json_err}")