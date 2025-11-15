# -*- coding: utf-8 -*- 
# """ Servidor NAO para recibir instrucciones desde Python 3 (modelo IA). Compatible con Python 2.7 y NAOqi. Movimientos + voz + mensaje de bienvenida + integración con Choregraphe. """
import socket
import threading
import sys
import time

sys.path.append("C:/Users/yamir/Desktop/PC_ML_NAO/pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649/lib")

from naoqi import ALProxy

NAO_IP = "127.0.0.1"
NAO_PORT = 65512
SERVER_PORT = 5000




tts = ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)
motion = ALProxy("ALMotion", NAO_IP, NAO_PORT)
posture = ALProxy("ALRobotPosture", NAO_IP, NAO_PORT)

def reset_postura_neutral():
    try:
        posture.goToPosture("StandInit", 0.8)
        names = ["LShoulderPitch", "RShoulderPitch", "LElbowRoll", "RElbowRoll",
                 "LShoulderRoll", "RShoulderRoll"]
        angles = [1.5, 1.5, -0.1, 0.1, 0.0, 0.0]
        times = [1.0] * len(names)
        motion.angleInterpolation(names, angles, times, True)
    except Exception as e:
        print("Error en reset_postura_neutral:", e)

def defensa_personal_brazos():
    try:
        names = ["LShoulderPitch", "RShoulderPitch", "LElbowRoll", "RElbowRoll"]
        angles = [0.5, 0.5, -1.0, 1.0]
        times = [1.0] * len(names)
        motion.angleInterpolation(names, angles, times, True)
    except Exception as e:
        print("Error en defensa_personal_brazos:", e)

def gesto_presentacion():
    try:
        tts.say("Hola, soy Nao. Activando detección de cercanía.")
        motion.setAngles(["LShoulderPitch", "RShoulderPitch"], [0.1, 0.1], 0.3)
        time.sleep(0.7)
        motion.setAngles(["LShoulderPitch", "RShoulderPitch"], [1.2, 1.2], 0.3)
        time.sleep(0.7)
        reset_postura_neutral()
    except Exception as e:
        print("Error en gesto_presentacion:", e)

def handle_client(conn, addr):
    print("Conexión desde:", addr)
    
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            try:
                msg = data.decode("utf-8").strip()
            except:
                msg = data.strip()

            print("Mensaje recibido:", msg)
           

            if msg == "FIST":
                
                tts.say("¡Alerta! Estás demasiado cerca")
                defensa_personal_brazos()
                conn.send("OK:FIST")

            elif msg == "NO_FIST":
                tts.say("No se detecta amenaza")
                
                reset_postura_neutral()
                conn.send("OK:NO_FIST")

            else:
                print("Mensaje desconocido:", msg)
                conn.send("UNKNOWN")

    except Exception as e:
        print("Error con cliente:", e)

    finally:
        conn.close()
        print("Conexión cerrada:", addr)

def start_server():
    print("Realizando gesto inicial de verificación...")
    gesto_presentacion()
    print("Gesto inicial completado. Esperando conexión del modelo...")
    print("=== Servidor NAO iniciado en puerto {} ===".format(SERVER_PORT))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", SERVER_PORT))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.daemon = True
        t.start()

if __name__ == "__main__":
    start_server()