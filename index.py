import cv2
import numpy as np
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
import threading
import time

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

object_count = 0  # Contador de rostros únicos detectados
detected_faces = {}  # Diccionario para almacenar rostros detectados
face_timeout = 5  # Tiempo en segundos para volver a contar un rostro

# Carga el modelo Haar Cascade para detección de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "count": object_count})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    global object_count
    prev_count = -1
    while True:
        if object_count != prev_count:
            await websocket.send_text(str(object_count))
            prev_count = object_count

def detectar_rostros(frame):
    global object_count

    # Convertir a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar rostros en la imagen
    rostros = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
    nuevos_rostros = {}
    current_time = time.time()

    for (x, y, w, h) in rostros:
        centro_x = x + w // 2
        centro_y = y + h // 2

        # Verificar si el rostro ya fue detectado recientemente
        rostro_detectado = False
        for timestamp, (px, py) in list(detected_faces.items()):
            distancia = np.sqrt((px - centro_x) ** 2 + (py - centro_y) ** 2)
            if distancia < 50:  # Si está cerca, es el mismo rostro
                if current_time - timestamp < face_timeout:
                    rostro_detectado = True
                    break
                else:
                    del detected_faces[timestamp]  # Eliminar rostros antiguos

        if not rostro_detectado:
            nuevos_rostros[current_time] = (centro_x, centro_y)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if nuevos_rostros:
        object_count += len(nuevos_rostros)
        print(f"🙂 Rostros detectados: {len(nuevos_rostros)}, Total: {object_count}")

    detected_faces.update(nuevos_rostros)

    return frame

def iniciar_deteccion():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = detectar_rostros(frame)
        cv2.imshow("Detección de Rostros", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

threading.Thread(target=iniciar_deteccion, daemon=True).start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
