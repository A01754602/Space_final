from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Inicializamos la aplicación Flask
app = Flask(__name__)

# Cargar el modelo
model = joblib.load("voting_model.joblib")

# Función para predicción
@app.route('/predictjson', methods=['POST'])
def predict():
    try:
        # Obtener los datos JSON del request
        input_data = request.get_json()
        print(f"Datos recibidos: {input_data}")

        # Convertir el JSON en un DataFrame de pandas
        df = pd.DataFrame([input_data])
        
        # Asegurar que las columnas están en el orden correcto
        df = df[['HomePlanet', 'CryoSleep', 'Destination', 'Age', 'VIP', 'RoomService', 
                 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck', 'Deck', 'Num', 'Side']]
        
        print(f"Datos para predicción: {df}")
        
        # Realizar la predicción
        prediction = model.predict(df)[0]
        print(f"Predicción: {prediction}")
        
        # Devolver el resultado en formato JSON
        return jsonify({'Prediction': bool(prediction)})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)