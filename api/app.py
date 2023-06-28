import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from datetime import datetime


app = FastAPI()

## Using Pydantic lib, defining the data type for all the inputs
class model_input(BaseModel):
    
    ph : float
    temperature : float 
    turbidity : float

model = joblib.load('modelss5.pkl')

@app.get('/')
async def home():
    return {'Hallo Manis, Fast Api nya sudah'}

@app.get('/predict')  # Allow GET requests for /predict endpoint
def get_predict():
    return {'message': 'Send a POST request to this endpoint to make predictions.'}

@app.post('/predict')
def predict_water_quality(data: model_input):
    # Ubah input data menjadi array numpy
    input_data = [[data.ph, data.temperature, data.turbidity]]
    
    # Lakukan prediksi dengan model
    prediction = model.predict(input_data)[0]
    
    # Ubah hasil prediksi menjadi label
    if prediction == 0:
        result = "Bersih"
    else:
        result = "Keruh"
    
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Kembalikan hasil prediksi
    return {
        "prediction": result,
        "datetime": current_datetime}

@app.get('/predict/{ph}/{temperature}/{turbidity}')
def get_prediction(ph: float, temperature: float, turbidity: float):
    # Ubah input data menjadi array numpy
    input_data = [[ph, temperature, turbidity]]

    # Lakukan prediksi dengan model
    prediction = model.predict(input_data)[0]

    # Ubah hasil prediksi menjadi label
    if prediction == 0:
        result = "Bersih"
    else:
        result = "Keruh"
        
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Kembalikan hasil prediksi
    return {
        "input": {
            "ph": ph,
            "temperature": temperature,
            "turbidity": turbidity
        },
        "prediction": result,
        "datetime": current_datetime
    }
    
if __name__  == '__main__':
  uvicorn.run("app:app", host= "localhost", port=5000,reload=True)