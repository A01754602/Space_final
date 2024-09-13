from flask import Flask, request, jsonify
import numpy as np
import joblib
from sklearn.preprocessing import MinMaxScaler

# Cargar el modelo entrenado 
model = joblib.load('voting_model.joblib')  # Modelo final

# Escalamiento de las variables
scaler = MinMaxScaler()

# Crear el servidor Flask
app = Flask(__name__)

# Definir la ruta
@app.route('/predictjson', methods=['POST'])
def predictjson():
    try:
        # Recibir los datos en formato JSON
        data = request.json  
        print("Datos recibidos:", data)  # Depurar los datos recibidos

        required_keys = ['HomePlanet', 'CryoSleep', 'Age', 'RoomService', 'FoodCourt',
                         'ShoppingMall', 'Spa', 'VRDeck', 'Destination', 'Deck', 'Side', 'Num', 'VIP']
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Falta el valor requerido: {key}")

        # Convertir los datos a un array numpy en el formato que el modelo espera
        input_data = np.array([
            data['HomePlanet'],
            data['CryoSleep'],
            data['Age'],
            data['RoomService'],
            data['FoodCourt'],
            data['ShoppingMall'],
            data['Spa'],
            data['VRDeck'],
            data['Destination'],
            data['Deck'],
            data['Side'],
            data['Num'],
            data['VIP']
        ]).reshape(1, -1)

        # Normalizar los datos antes de hacer la predicción
        input_data_scaled = scaler.fit_transform(input_data)

        # Realizar la predicción utilizando el modelo final
        prediction = model.predict(input_data_scaled)

        # Devolver la predicción como JSON
        return jsonify({'Prediction': bool(prediction[0])})

    except ValueError as ve:
        print(f"Error de valor: {str(ve)}")  
        return jsonify({'error': str(ve)}), 400  

    except Exception as e:
        print(f"Error en la predicción: {str(e)}")  
        return jsonify({'error': str(e)}), 500  

# Iniciar el servidor Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)