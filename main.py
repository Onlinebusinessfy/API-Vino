from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import numpy as np
from tensorflow import keras  # Importar keras en lugar de joblib

# Inicializa la aplicación
app = FastAPI()

# Permite el acceso CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes de cualquier origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta la carpeta estática para servir archivos HTML y JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Carga el modelo de calidad del vino
model = keras.models.load_model('wine_quality_model.h5')  # Cambia a keras.models.load_model

# Clase para validar la entrada de datos
class WineData(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float

# Ruta para el archivo HTML
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html") as f:
        return f.read()

# Ruta para hacer predicciones
@app.post("/predict")
async def predict(wine_data: WineData):
    # Convertir la entrada en un array numpy
    wine_array = np.array([[wine_data.fixed_acidity,
                            wine_data.volatile_acidity,
                            wine_data.citric_acid,
                            wine_data.residual_sugar,
                            wine_data.chlorides,
                            wine_data.free_sulfur_dioxide,
                            wine_data.total_sulfur_dioxide,
                            wine_data.density,
                            wine_data.pH,
                            wine_data.sulphates,
                            wine_data.alcohol]])

    # Realizar la predicción
    try:
        prediction = model.predict(wine_array)
        predicted_quality = float(prediction[0][0])  # Asegúrate de que el valor sea un float
        return {"quality": predicted_quality}  # Devuelve la calidad predicha
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {str(e)}")
