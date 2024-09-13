import streamlit as st
import numpy as np
import requests

# Establecer título y estilo de la página
st.set_page_config(page_title="Spaceship Titanic - Supervivencia", page_icon="🚀")

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
st.title("🪐 Predicción de Supervivencia en el Titanic Espacial 🛸")

# Subtítulo con un breve texto
st.subheader("🚀 ¿Sobrevivirías el viaje interestelar? Descúbrelo con nuestro modelo de predicción 🤖")

# Crear sliders y selectboxes con emojis espaciales
home_planet = st.selectbox("🌍 Planeta de origen", ["Earth", "Europa", "Mars"])
cryosleep = st.radio("❄️ ¿Estaba en Criosueño?", ["Sí", "No"])
age = st.slider("👶 Edad", 0, 100, 30)
room_service = st.slider("🛎️ Room Service", 0, 10000, 0)
food_court = st.slider("🍔 Food Court", 0, 10000, 0)
shopping_mall = st.slider("🛒 Shopping Mall", 0, 10000, 0)
spa = st.slider("🛀 Spa", 0, 10000, 0)
vr_deck = st.slider("🎮 VR Deck", 0, 10000, 0)
destination = st.selectbox("🌌 Destino", ["TRAPPIST-1e", "55 Cancri e", "PSO J318.5-22"])
deck = st.selectbox("🛳️ Deck", ["A", "B", "C", "D", "E", "F", "G", "T"])
side = st.selectbox("🔄 Side", ["P", "S"])
num = st.number_input("🔢 Número de Cabina", min_value=0, max_value=2000, step=1)

# Botón para predecir con efecto hover
if st.button("🌟 Predecir Supervivencia"):
    # Convertir las entradas a los valores correctos que el modelo espera
    cryosleep_val = 1 if cryosleep == "Sí" else 0
    home_planet_val = {"Earth": 0.424, "Europa": 0.626, "Mars": 0.5586}[home_planet]
    destination_val = {"TRAPPIST-1e": 0.4711, "55 Cancri e": 0.61, "PSO J318.5-22": 0.5037}[destination]
    deck_val = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "T": 7}[deck]
    side_val = {"P": 0, "S": 1}[side]

    # Crear el JSON con los datos
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
        "Num": num
    }

    FLASK_API_URL = "http://34.229.203.135:8080/predictjson"

    try:
        response = requests.post(FLASK_API_URL, json=input_data)
        response.raise_for_status()  # Verifica que no hubo un error HTTP
        prediction = response.json().get('Prediction')

        if prediction == 'True':
            st.success('🟢 ¡El pasajero sobrevivirá la aventura espacial! 🎉')
        else:
            st.error('🔴 Desafortunadamente, el pasajero no sobrevivirá. 💫')
    
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")  # Muestra el error HTTP
    except requests.exceptions.RequestException as err:
        st.error(f"Error occurred: {err}")  # Muestra otros errores de solicitud
    except ValueError as json_err:
        st.error(f"Error al decodificar la respuesta JSON: {json_err}")  # Muestra errores de decodificación JSON
        st.text(response.text)  # Muestra la respuesta recibida (aunque no sea JSON)

# Pie de página con información adicional
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("✨ *AAAAAAAAAAAAA* 🛸")