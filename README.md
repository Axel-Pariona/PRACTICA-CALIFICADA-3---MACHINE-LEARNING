# **PC3 – Detección de golpes con NAO (Fist vs No_fist)**

**Curso:** Machine Learning — UPC  
**Práctica:** PC3 — Detección de golpes y reacción física con NAO  
**Integrantes:** Omar Acuña Villegas, Axel Yamir Pariona Rojas, Marcelo Paolo Murguia Lozano  
**Fecha:** Noviembre 2025  

---

## **Objetivo del Proyecto**

El objetivo de este proyecto es desarrollar e integrar un modelo de Machine Learning supervisado (clasificación binaria: **fist** / **no_fist**) en el robot humanoide **NAO**.  
El sistema detecta golpes mediante visión por computadora y ejecuta una acción física coherente:

- **Fist →** El NAO adopta una postura defensiva y emite un mensaje de alerta.  
- **No_fist →** El NAO permanece en postura neutral.  

El flujo completo (captura → predicción → acción física) se ejecuta de manera automática, cumpliendo los requisitos de la PC3.

---

## **Contenido del Repositorio**

- `src/Trainmodel_PY3.py` → Entrenamiento del modelo con MobileNetV2.  
- `src/predict_and_send.py` → Predicción en tiempo real + envío por socket al NAO.  
- `src/nao-server.py` → Servidor en NAO: recibe predicción y ejecuta acciones físicas.  
- `src/Mark2.py` → Posturas defensivas y movimientos del robot.  
- `src/NAO_PC3_pasado.py` → Versiones previas / pruebas iniciales.  
- `models/model_fist_detection.h5` → Modelo entrenado final.  
- `DATASET/` → Dataset original (gestos de manos).  
- `tmp_binarized_dataset/` → Dataset convertido a fist/no_fist.  
- `results/accuracy_curve.png` → Curva de precisión del entrenamiento.  
- `results/loss_curve.png` → Curva de pérdida del entrenamiento.  
- `architecture_diagram.mmd` → Diagrama de arquitectura (Mermaid).  
- `docs/report.pdf` → Informe final del proyecto.

---

## **Descripción detallada de cada componente**

###  **1. Trainmodel_PY3.py**
Entrena el modelo de visión usando MobileNetV2 con transfer learning.  
Incluye:
- carga y binarización del dataset  
- aumentación de datos  
- callbacks (ModelCheckpoint, EarlyStopping, LR scheduler)  
- guardado del modelo `.h5`  
- generación de curvas de accuracy y loss  

---

###  **2. predict_and_send.py**
Captura imágenes desde webcam o NAO.  
Hace:
- preprocesamiento (resize 224×224, normalización)  
- predicción usando el modelo entrenado  
- envío de resultado al NAO mediante sockets TCP  

---

###  **3. nao-server.py**
Corre en la PC conectada al robot.  
Funciones:
- recibe “fist” o “no_fist”  
- ejecuta postura defensiva o postura neutral  
- usa API de **pynaoqi** para mover articulaciones  
- genera mensajes de voz (TTS)

---

###  **4. Mark2.py**
Contiene:
- posiciones del robot  
- animaciones defensivas  
- posiciones neutrales  
- tiempos y secuencias  

---

###  **5. DATASET y tmp_binarized_dataset**
- dataset original con distintas clases (“fist”, “five”, “rad”, “peace”, …)  
- dataset convertido solo a **fist / no_fist**  
- compatible con ImageDataGenerator  

---

## **Diagrama de Arquitectura**

```mermaid
flowchart LR
  A[Camara NAO / Webcam] --> B[Preprocesamiento (resize, rescale)]
  B --> C[Modelo - MobileNetV2]
  C --> D{Predicción}
  D -->|FIST| E[Socket → NAO]
  D -->|NO_FIST| F[Postura neutral]
  E --> G[NAO: Postura defensiva + voz]
