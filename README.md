# ```markdown

# \# PC3 - Detección de golpes con NAO (Fist vs No\_fist)

# 

# \*\*Curso:\*\* Machine Learning — UPC  

# \*\*Práctica:\*\* PC3 — Detección de golpes y reacción física con NAO  

# \*\*Integrantes:\*\* Omar Acuña Villegas, Axel Yamir Pariona Rojas, Marcelo Paolo Murguia Lozano  

# \*\*Fecha:\*\* Noviembre 2025

# 

# ---

# 

# \## Objetivo

# Desarrollar e integrar un modelo de Machine Learning supervisado (clasificación binaria: \*fist\* / \*no\_fist\*) en el robot humanoide NAO. El sistema detecta golpes a través de la visión, y condiciona la acción física del robot (voz + postura defensiva) a la predicción.

# 

# ---

# 

# \## Contenido del repositorio

# \- `src/Trainmodel\_PY3.py` — Script de entrenamiento (transfer learning con MobileNetV2).

# \- `src/predict\_and\_send.py` — Predicción en tiempo real y envío de señal al NAO (socket).

# \- `src/nao-server.py` — Servidor que corre junto al NAO y recibe mensajes para ejecutar acciones.

# \- `src/Mark2.py`, `src/NAO\_PC3\_pasado.py` — Scripts de manejo de posturas y secuencias de voz.

# \- `models/model\_fist\_detection.h5` — Modelo entrenado (incluir si no es muy grande).

# \- `DATASET/` — Estructura del dataset (train/valid/test).

# \- `tmp\_binarized\_dataset/` — Estructura temporal utilizada por el `Trainmodel\_PY3.py`.

# \- `results/accuracy\_curve.png`, `results/loss\_curve.png` — Curvas de entrenamiento.

# \- `architecture\_diagram.mmd` — Diagrama de arquitectura (Mermaid).

# \- `docs/report.pdf` — Informe final (PDF).

# 

# ---

# 

# \## Diagrama de arquitectura

# > Flujo: Cámara → Preprocesamiento → Modelo → Predicción → NAO (acción física).

# 

# ---

# 

# \## Instalación y dependencias

# 

# ```bash

# python -m venv venv

# source venv/bin/activate   # Linux/Mac

# \# .\\venv\\Scripts\\activate  # Windows

# pip install -r requirements.txt



