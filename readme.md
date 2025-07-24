# Instala las dependencias:
  pip install fastapi uvicorn opencv-python numpy
  pip install jinja2

# Ejecuta el backend:
  python index.py

# Abre tu navegador y ve a:
  http://127.0.0.1:8000/

************************************************************************************

# 1. Pasos para Entrenar un Modelo
  Recolectar imágenes, mínimo 300 imágenes del objeto que quieres detectar desde distintos ángulos y condiciones de iluminación.

# 2. Etiquetar las imágenes
  Las imágenes deben estar anotadas con las coordenadas del objeto dentro de cada imagen.
    🛠 Herramientas para etiquetar:
        LabelImg (Interfaz gráfica, fácil de usar) → Instalación
        Roboflow Annotate (Online, sincroniza con modelos YOLO)
        CVAT (Más avanzada)

# 3. Preparar el dataset
  Una vez anotadas las imágenes, debes dividirlas en:
    80% para entrenamiento
    20% para validación

# 4.Configurar el archivo de datos para YOLOv8


# 5.Entrenar el modelo con YOLOv8