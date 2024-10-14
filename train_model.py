import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers

# Cargar el conjunto de datos
data = pd.read_csv('C:/Users/fache/Desktop/API de calidad del vino/WineQT.csv')  # Cambia esto a la ubicación de tu archivo

# Separar características y variable objetivo
X = data.drop(columns=['quality', 'Id'])  # Excluye la columna de calidad y el ID
y = data['quality']

# Dividir el conjunto de datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Estandarizar los datos
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Crear el modelo de deep learning
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    layers.Dense(64, activation='relu'),
    layers.Dense(1)  # Salida para regresión
])

model.compile(optimizer='adam', loss='mean_squared_error')

# Entrenar el modelo
model.fit(X_train, y_train, epochs=100, validation_split=0.2)

# Guardar el modelo
model.save('wine_quality_model.h5')
