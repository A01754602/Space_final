from flask import Flask, request, jsonify
import numpy as np
import joblib

# Cargar el modelo de votación entrenado
model = joblib.load('voting_model.joblib')

# Obtener los nombres de las características utilizadas durante el entrenamiento
feature_names = model.feature_names_in_  # Este atributo contiene los nombres originales de las características

# Crear la aplicación Flask
app = Flask(__name__)

# Definir la ruta de predicción
@app.route('/predictjson', methods=['POST'])
def predictjson():
    try:
        # Recibir los datos en formato JSON
        data = request.json  
        print("Datos recibidos:", data)  # Depurar los datos recibidos

        # Reorganizar los datos según el orden correcto de características
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
        ])

        # Realizar la predicción utilizando el modelo cargado
        prediction = model.predict(input_data.reshape(1, -1))
        probabilities = model.predict_proba(input_data.reshape(1, -1))

        # Devolver la predicción y probabilidades como JSON
        return jsonify({'Prediction': bool(prediction[0]), 'Probabilities': probabilities.tolist()})

    except ValueError as ve:
        print(f"Error de valor: {str(ve)}")
        return jsonify({'error': str(ve)}), 400  # Retornar un error 400 si faltan datos o son incorrectos

    except Exception as e:
        print(f"Error en la predicción: {str(e)}")
        return jsonify({'error': str(e)}), 500  # Retornar un error 500 para otros errores

# Iniciar el servidor Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)