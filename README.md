# **PC3 – Detección de golpes con NAO (Fist vs No_fist)**

**Curso:** Machine Learning — UPC  
**Práctica:** PC3 — Detección de golpes y reacción física con NAO  
**Integrantes:** Omar Acuña Villegas, Axel Yamir Pariona Rojas, Marcelo Paolo Murguia Lozano  
**Fecha:** Noviembre 2025  

---

## **Objetivo del Proyecto**

El objetivo de este proyecto es desarrollar e integrar un modelo de Machine Learning supervisado (clasificación binaria: **fist** / **no_fist**) en el robot humanoide **NAO**.  
El sistema detecta golpes mediante visión por computadora y ejecuta una acción física coherente:

- Si detecta **fist** → El NAO adopta una postura defensiva y emite un mensaje de alerta.  
- Si detecta **no_fist** → El NAO permanece en postura neutral.

El flujo completo (captura → predicción → acción) se ejecuta de manera **automática y sin intervención manual**, cumpliendo los requisitos de la PC3.

---

## **Contenido del repositorio**

- `src/Trainmodel_PY3.py` — Script de entrenamiento del modelo (MobileNetV2 con Transfer Learning).  
- `src/predict_and_send.py` — Script de predicción en tiempo real y envío de resultados al NAO vía socket.  
- `src/nao-server.py` — Servidor que recibe la predicción y ejecuta acciones en el robot.  
- `src/Mark2.py` — Acciones y posturas defensivas configuradas en NAO.  
- `src/NAO_PC3_pasado.py` — Versión alternativa y pruebas de integración.  
- `models/model_fist_detection.h5` — Modelo entrenado (si aplica).  
- `DATASET/` — Estructura completa del dataset (train / valid / test).  
- `tmp_binarized_dataset/` — Dataset convertido a binario para el entrenamiento (fist/no_fist).  
- `results/accuracy_curve.png` — Curva de precisión del entrenamiento.  
- `results/loss_curve.png` — Curva de pérdida del entrenamiento.  
- `architecture_diagram.mmd` — Diagrama de arquitectura en Mermaid.  
- `docs/report.pdf` — Informe completo en PDF.

---

## **Diagrama de Arquitectura**

> Flujo general:  
> **Cámara → Preprocesamiento → Modelo → Predicción → Comunicación Socket → NAO (Postura + Voz)**

Código Mermaid visualizable en GitHub:

```mermaid
flowchart LR
  A[Camara NAO / Webcam] --> B[Preprocesamiento (resize, rescale)]
  B --> C[Modelo - MobileNetV2 (h5)]
  C --> D{Predicción}
  D -->|FIST| E[Control NAO (socket)]
  D -->|NO_FIST| F[Postura neutral]
  E --> G[NAO - TTS y postura defensiva]

  subgraph Offline - Training
    H[Entrenamiento: Trainmodel_PY3.py]
    H --> C
    I[Curvas de entrenamiento (accuracy/loss)]
  end
