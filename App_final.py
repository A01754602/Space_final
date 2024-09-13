import streamlit as st
import numpy as np
import requests

# Establecer título y estilo de la página
st.set_page_config(page_title="Spaceship Titanic :)", page_icon="🚀")

# CSS para darle estilo espacial
page_bg_img = '''
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
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Título con diseño temático
st.title("🪐 Spaceship Titanic :) 🛸")

# Subtítulo con un breve texto
st.subheader("🚀 ¿Sobrevivirías el viaje interestelar? Descúbrelo con nuestro modelo de predicción 🤖")

home_planet = st.selectbox("🌍 Planeta de origen", ["Earth", "Europa", "Mars"])
cryosleep = st.radio("❄️ ¿Estaba en Criosueño?", ["Sí", "No"])
destination = st.selectbox("🌌 Destino", ["TRAPPIST-1e", "55 Cancri e", "PSO J318.5-22"])
deck = st.selectbox("🛳️ Deck", ["A", "B", "C", "D", "E", "F", "G", "T"])
side = st.selectbox("🔄 Side", ["P", "S"])
vip = st.radio("💎 ¿El pasajero es VIP?", ["Sí", "No"])

# Crear inputs manuales para valores numéricos
age = st.number_input("👶 Edad", min_value=0, max_value=100, value=30, step=1)
room_service = st.number_input("🛎️ Room Service", min_value=0, max_value=10000, value=0, step=1)
food_court = st.number_input("🍔 Food Court", min_value=0, max_value=10000, value=0, step=1)
shopping_mall = st.number_input("🛒 Shopping Mall", min_value=0, max_value=10000, value=0, step=1)
spa = st.number_input("🛀 Spa", min_value=0, max_value=10000, value=0, step=1)
vr_deck = st.number_input("🎮 VR Deck", min_value=0, max_value=10000, value=0, step=1)
num = st.number_input("🔢 Número de Cabina", min_value=0, max_value=2000, value=0, step=1)

if st.button("🌟 Predecir si sobrevive"):
    # Convierte los valores a las entradas esperadas del modelo
    cryosleep_val = 1 if cryosleep == "Sí" else 0
    home_planet_val = {"Earth": 0.424, "Europa": 0.626, "Mars": 0.5586}[home_planet]
    destination_val = {"TRAPPIST-1e": 0.4711, "55 Cancri e": 0.61, "PSO J318.5-22": 0.5037}[destination]
    deck_val = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "T": 7}[deck]
    side_val = {"P": 0, "S": 1}[side]
    vip_val = 1 if vip == "Sí" else 0

    # Enviar los datos al servidor Flask
    input_data = {
        "HomePlanet": home_planet_val,
        "CryoSleep": cryosleep_val,
        "Age": age,
        "RoomService": room_service,
        "FoodCourt": food_court,
        "ShoppingMall": shopping_mall,
        "Spa": spa,
        "VRDeck": vr_deck,
        "Destination": destination_val,
        "Deck": deck_val,
        "Side": side_val,
        "Num": num,
        "VIP": vip_val  
    }

    FLASK_API_URL = "http://34.228.165.103:8080/predictjson"  

    try:
        response = requests.post(FLASK_API_URL, json=input_data)
        response.raise_for_status()  # Verifica que no hubo un error HTTP
        prediction = response.json().get('Prediction')

        # Mostrar el resultado de la predicción
        if prediction:
            st.success('🟢 ¡El pasajero sobrevivirá! 🎉')
        else:
            st.error('🔴 Desafortunadamente, el pasajero no sobrevivirá :(')
    
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")  # Muestra el error HTTP
    except requests.exceptions.RequestException as err:
        st.error(f"Error occurred: {err}")  # Muestra otros errores de solicitud
    except ValueError as json_err:
        st.error(f"Error al decodificar la respuesta JSON: {json_err}")  # Muestra errores de decodificación JSON
        st.text(response.text)  # Muestra la respuesta recibida (aunque no sea JSON)

# Pie de página con información adicional
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(" *AAAAAAAAAAAAA*")