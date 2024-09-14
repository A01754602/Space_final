import pandas as pd
from flask import Flask, request, jsonify
import joblib

# Cargar el modelo de votación entrenado
model = joblib.load('voting_model.joblib')

# Crear la aplicación Flask
app = Flask(__name__)

# Definir la ruta de predicción
@app.route('/predictjson', methods=['POST'])
def predictjson():
    try:
        # Recibir los datos en formato JSON
        data = request.json  
        print("Datos recibidos:", data)  # Depuración de los datos recibidos

        # Convertir los datos en un DataFrame y asegurarse de que las columnas estén en el orden correcto
        input_data = pd.DataFrame([data], columns=[
            'HomePlanet', 'CryoSleep', 'Destination', 'Age', 'RoomService', 
            'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck', 'Deck', 'Side', 'Num', 'VIP'
        ])
        print("Datos para predicción:", input_data)  # Verificar el DataFrame
        
        # Realizar la predicción utilizando el modelo cargado
        prediction = model.predict(input_data)

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