# detect_fist.py
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import socket
import time # ¡Nuevo!

# === CONFIGURACIÓN ===
MODEL_PATH = "model_fist_detection.h5"
IMG_SIZE = (160, 160)
NAO_IP = "127.0.0.1"
NAO_PORT = 5000

# === PARÁMETROS DE DELAY ===
# Define cuánto tiempo debe esperar el cliente (en segundos) antes de enviar otro mensaje.
COOLDOWN_DELAY = 10
ultimo_envio = 0.0 # Variable para registrar la hora del último envío

# === CARGA DEL MODELO ===
model = load_model(MODEL_PATH)

# === CONFIGURAR CONEXIÓN CON NAO ===
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((NAO_IP, NAO_PORT))
    print("✅ Conectado con NAO correctamente.")
except:
    client_socket = None
    print("⚠️ No se pudo conectar con NAO. Continuando en modo local.")

# === INICIAR CÁMARA ===
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocesar imagen
    img = cv2.resize(frame, IMG_SIZE)
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)

    # Predicción
    prediction = model.predict(img)
    label = "FIST" if prediction[0][0] > 0.5 else "NEUTRAL"

    # Mostrar resultado en la pantalla
    cv2.putText(frame, f"Prediction: {label}", (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
    cv2.imshow("Fist Detection", frame)

    # =================================================================
    # === LÓGICA DE DELAY Y ENVÍO (¡Modificado aquí!) ===
    # =================================================================
    ahora = time.time()
    
    # Solo intentamos enviar si el socket está conectado Y ha pasado el tiempo de espera
    if client_socket and (ahora - ultimo_envio) >= COOLDOWN_DELAY:
        
        # En tu código anterior, envías 'defensa' o 'neutral', pero el servidor NAO 
        # espera 'FIST' o 'NO_FIST'. Usaremos los mensajes que espera el servidor.
        
        msg_to_send = b"FIST" if label == "FIST" else b"NO_FIST"
        
        try:
            client_socket.sendall(msg_to_send)
            print(f"Enviado: {msg_to_send.decode()} - Próximo envío en {COOLDOWN_DELAY}s.")
            ultimo_envio = ahora # ¡Actualiza la hora del último envío exitoso!
        except socket.error as e:
            print(f"Error de socket al enviar: {e}. Desconectando...")
            client_socket.close()
            client_socket = None # Deshabilita el envío si falla
    # =================================================================

    # Salir con tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if client_socket:
    client_socket.close()