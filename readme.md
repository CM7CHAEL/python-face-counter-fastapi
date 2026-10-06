# Contador de rostros en tiempo real

Cuenta las personas que pasan frente a la cámara y publica el total en vivo en una página web.

- **Detección:** OpenCV con el clasificador Haar Cascade de rostros frontales.
- **Sin contar dos veces a la misma persona:** cada rostro se registra por la posición de su centro;
  si aparece otro a menos de 50 px dentro de una ventana de 5 s, se considera el mismo.
- **Total en vivo:** FastAPI expone un WebSocket (`/ws`) que empuja el contador a la página sin recargarla.
- La detección corre en un hilo aparte, así el servidor web sigue respondiendo.

## Cómo correrlo

```bash
pip install fastapi uvicorn opencv-python numpy jinja2
mkdir templates static
cp index.html templates/
python index.py
```

Abre http://127.0.0.1:8000/ y mira el contador. Se abre también una ventana con la cámara y los
rostros marcados; se cierra con `q`.

## Siguiente paso: entrenar un detector propio con YOLOv8

Haar Cascade solo sirve para rostros. Para contar otro objeto (celulares, cajas, vehículos) hay que
entrenar un modelo:

1. **Recolectar imágenes:** mínimo 300 del objeto, desde distintos ángulos y con distinta iluminación.
2. **Etiquetarlas** con las coordenadas del objeto en cada imagen. Herramientas:
   - LabelImg: interfaz gráfica, fácil de usar.
   - Roboflow Annotate: en línea, exporta directo al formato YOLO.
   - CVAT: la más completa.
3. **Separar el dataset:** 80 % para entrenamiento y 20 % para validación.
4. **Configurar** el archivo de datos de YOLOv8 con las rutas y las clases.
5. **Entrenar** el modelo con YOLOv8 y reemplazar el Haar Cascade por el modelo entrenado.

## Stack
Python · OpenCV · FastAPI · WebSockets · Jinja2
