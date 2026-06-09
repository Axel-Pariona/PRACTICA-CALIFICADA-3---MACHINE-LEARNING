# -*- coding: utf-8 -*-
from naoqi import ALProxy
import time
import cv2
import numpy as np

# =======================
# CONFIGURACIÓN DE CONEXIÓN
# =======================
NAO_IP = "127.0.0.1"   # IP del NAO o localhost si es simulador
PORT = 60632

# Crear proxies
tts = ALProxy("ALTextToSpeech", NAO_IP, PORT)
motion = ALProxy("ALMotion", NAO_IP, PORT)
posture = ALProxy("ALRobotPosture", NAO_IP, PORT)
videoProxy = ALProxy("ALVideoDevice", NAO_IP, PORT)

motion.wakeUp()

# =======================
# FUNCIONES DE MOVIMIENTO
# =======================
def reset_postura_neutral():
    """Postura inicial: de pie, brazos abajo relajados."""
    names = ["LShoulderPitch", "RShoulderPitch", "LElbowRoll", "RElbowRoll",
             "LShoulderRoll", "RShoulderRoll"]
    angles = [1.5, 1.5, -0.1, 0.1, 0.0, 0.0]
    times = [1.0] * len(names)
    motion.angleInterpolation(names, angles, times, True)
    time.sleep(0.5)

def defensa_personal_brazos():
    """Postura defensiva (brazos recogidos)."""
    names = ["LShoulderPitch", "RShoulderPitch", "LElbowRoll", "RElbowRoll"]
    angles = [0.5, 0.5, -1.0, 1.0]
    times = [1.0] * len(names)
    motion.angleInterpolation(names, angles, times, True)
    time.sleep(0.5)

def gesto_ambos_brazos_ataque():
    """Simula golpes alternos con ambos brazos."""
    motion.setAngles(["RShoulderPitch", "RElbowRoll"], [0.1, 0.8], 0.3)
    time.sleep(0.5)
    motion.setAngles(["RShoulderPitch", "RElbowRoll"], [1.2, 1.0], 0.2)
    time.sleep(0.5)
    motion.setAngles(["LShoulderPitch", "LElbowRoll"], [0.1, -0.8], 0.3)
    time.sleep(0.5)
    motion.setAngles(["LShoulderPitch", "LElbowRoll"], [1.2, -1.0], 0.2)
    time.sleep(0.5)
    defensa_personal_brazos()

# =======================
# DETECCIÓN DE CERCANÍA CON LA CÁMARA
# =======================
def detectar_cercania():
    """Detecta la cercanía de una persona con la cámara del NAO (OpenCV)."""
    # Carga el clasificador facial
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        print("⚠️ No se encontró el archivo haarcascade_frontalface_default.xml")
        return

    # Suscribirse a la cámara
    resolution = 2   # 640x480
    colorSpace = 11  # kBGRColorSpace
    fps = 10
    videoClient = videoProxy.subscribeCamera("python_client", 0, resolution, colorSpace, fps)

    try:
        while True:
            naoImage = videoProxy.getImageRemote(videoClient)
            if naoImage is None:
                continue

            width, height = naoImage[0], naoImage[1]
            array = naoImage[6]

            # En Python 2.7, convertir el buffer de forma distinta
            frame = np.fromstring(array, dtype=np.uint8)
            frame = frame.reshape((height, width, 3))

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rostros = face_cascade.detectMultiScale(gray, 1.3, 5)

            # Dibujar y reaccionar
            for (x, y, w, h) in rostros:
                area = w * h
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                if area > 25000:
                    print("Persona MUY cerca -> defensa agresiva")
                    tts.say("Alerta de proximidad detectada.")
                    gesto_ambos_brazos_ataque()
                elif area > 10000:
                    print("Persona cerca -> postura defensiva")
                    tts.say("Me pondré en guardia.")
                    defensa_personal_brazos()
                else:
                    print("Persona lejos -> postura neutral")
                    reset_postura_neutral()

            # Mostrar imagen (solo si tienes pantalla)
            cv2.imshow("Camara NAO", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Interrupción del usuario.")
    finally:
        videoProxy.unsubscribe(videoClient)
        cv2.destroyAllWindows()

# =======================
# PROGRAMA PRINCIPAL
# =======================
tts.say("Hola, soy Nao. Activando detección de cercanía.")
reset_postura_neutral()
time.sleep(1)

detectar_cercania()
