import streamlit as st
import numpy as np
import requests
from sklearn.preprocessing import MinMaxScaler

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

# Crear selectboxes y entradas numéricas manuales
home_planet = st.selectbox("🌍 Planeta de origen", ["Earth", "Europa", "Mars"])
cryosleep = st.radio("❄️ ¿Estaba en Criosueño?", ["Sí", "No"])
age = st.number_input("👶 Edad", min_value=0, max_value=100, value=30)
room_service = st.number_input("🛎️ Room Service", min_value=0, max_value=10000, value=0, step=10)
food_court = st.number_input("🍔 Food Court", min_value=0, max_value=10000, value=0, step=10)
shopping_mall = st.number_input("🛒 Shopping Mall", min_value=0, max_value=10000, value=0, step=10)
spa = st.number_input("🛀 Spa", min_value=0, max_value=10000, value=0, step=10)
vr_deck = st.number_input("🎮 VR Deck", min_value=0, max_value=10000, value=0, step=10)
destination = st.selectbox("🌌 Destino", ["TRAPPIST-1e", "55 Cancri e", "PSO J318.5-22"])
deck = st.selectbox("🛳️ Deck", ["A", "B", "C", "D", "E", "F", "G", "T"])
side = st.selectbox("🔄 Side", ["P", "S"])
num = st.number_input("🔢 Número de Cabina", min_value=0, max_value=2000, value=0, step=1)
vip = st.radio("💎 ¿El pasajero es VIP?", ["Sí", "No"])  # Nueva opción para VIP

# Botón para predecir con efecto hover
if st.button("🌟 Predecir Supervivencia"):
    # Convertir las entradas a los valores correctos que el modelo espera
    cryosleep_val = 1 if cryosleep == "Sí" else 0
    home_planet_val = {"Earth": 0.424, "Europa": 0.626, "Mars": 0.5586}[home_planet]
    destination_val = {"TRAPPIST-1e": 0.4711, "55 Cancri e": 0.61, "PSO J318.5-22": 0.5037}[destination]
    deck_val = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "T": 7}[deck]
    side_val = {"P": 0, "S": 1}[side]
    vip_val = 1 if vip == "Sí" else 0  # Convertir VIP a valor numérico

    # Crear el array de las variables numéricas
    input_data = np.array([
        age,
        room_service,
        food_court,
        shopping_mall,
        spa,
        vr_deck,
        num
    ]).reshape(1, -1)

    # Aplicar MinMaxScaler para estandarizar los valores
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(input_data)  # Escalar las variables numéricas

    # Preparar los datos estandarizados y categóricos en un diccionario
    input_data_scaled = {
        "HomePlanet": home_planet_val,
        "CryoSleep": cryosleep_val,
        "Age": scaled_data[0][0],
        "RoomService": scaled_data[0][1],
        "FoodCourt": scaled_data[0][2],
        "ShoppingMall": scaled_data[0][3],
        "Spa": scaled_data[0][4],
        "VRDeck": scaled_data[0][5],
        "Destination": destination_val,
        "Deck": deck_val,
        "Side": side_val,
        "Num": scaled_data[0][6],
        "VIP": vip_val  # Incluir VIP en los datos enviados
    }

    FLASK_API_URL = "http://34.228.165.103:8080/predictjson"

    try:
        response = requests.post(FLASK_API_URL, json=input_data_scaled)
        response.raise_for_status()  # Verifica que no hubo un error HTTP
        prediction = response.json().get('Prediction')

        # Verificar si la predicción es 1 o 'True'
        if prediction in [1, 'True', True]:
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