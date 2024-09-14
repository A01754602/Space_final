from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import joblib

# Cargar el modelo de votación entrenado
model = joblib.load('voting_model.joblib')  # Cargar el modelo previamente guardado

# Crear la aplicación Flask
app = Flask(__name__)

# Definir el orden correcto de las características, tal como fue durante el entrenamiento
FEATURE_ORDER = ['HomePlanet', 'CryoSleep', 'Destination', 'Age', 'RoomService', 'FoodCourt', 
                 'ShoppingMall', 'Spa', 'VRDeck', 'Deck', 'Side', 'Num', 'VIP']

# Definir la ruta de predicción
@app.route('/predictjson', methods=['POST'])
def predictjson():
    try:
        # Recibir los datos en formato JSON
        data = request.json  
        print("Datos recibidos:", data)  # Depurar los datos recibidos

        # Convertir los datos a un DataFrame de pandas con las características en el orden correcto
        input_data = pd.DataFrame([[
            data['HomePlanet'],
            data['CryoSleep'],
            data['Destination'],
            data['Age'],
            data['RoomService'],
            data['FoodCourt'],
            data['ShoppingMall'],
            data['Spa'],
            data['VRDeck'],
            data['Deck'],
            data['Side'],
            data['Num'],
            data['VIP']
        ]], columns=FEATURE_ORDER)

        print("Datos para predicción:", input_data)

        # Realizar la predicción utilizando el modelo cargado
        prediction = model.predict(input_data)

        # Devolver la predicción como JSON
        return jsonify({'Prediction': bool(prediction[0])})

    except ValueError as ve:
        print(f"Error de valor: {str(ve)}")  # Depuración de errores en la entrada de datos
        return jsonify({'error': str(ve)}), 400  # Retornar un error 400 si faltan datos

    except Exception as e:
        print(f"Error en la predicción: {str(e)}")  # Depuración de errores generales
        return jsonify({'error': str(e)}), 500  # Retornar un error 500 para otros errores

# Iniciar el servidor Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)