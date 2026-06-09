# NAO Fist Detection ML

NAO Fist Detection ML es un proyecto académico de Machine Learning y robótica que integra un modelo de visión por computadora con el robot humanoide **NAO**. El sistema clasifica imágenes en dos categorías, **fist** y **no_fist**, y envía el resultado a un servidor conectado al robot para ejecutar una respuesta física o verbal.

El proyecto fue desarrollado como práctica académica del curso de Machine Learning, combinando clasificación de imágenes, transferencia de aprendizaje con MobileNetV2, comunicación por sockets TCP e interacción con NAO mediante NAOqi.

## Video de demostración

La siguiente demostración muestra el flujo general del proyecto: detección visual, envío de predicción y reacción del robot NAO.

[![Ver demostración en YouTube](https://img.youtube.com/vi/F_7UR1QY6-U/maxresdefault.jpg)](https://youtu.be/F_7UR1QY6-U)

Enlace directo: https://youtu.be/F_7UR1QY6-U

## Objetivo del proyecto

El objetivo principal es entrenar e integrar un modelo de clasificación binaria capaz de detectar si una imagen corresponde a un gesto de puño (**fist**) o a otra clase de gesto (**no_fist**), para luego comunicar la predicción a un módulo de control del robot NAO.

El proyecto busca demostrar:

- Entrenamiento de un modelo de visión por computadora.
- Uso de transferencia de aprendizaje con MobileNetV2.
- Clasificación binaria de imágenes.
- Uso de OpenCV para captura en tiempo real.
- Comunicación por sockets entre el cliente de predicción y el servidor del robot.
- Integración con NAOqi para ejecutar voz y movimientos.
- Organización del flujo completo entre modelo, predicción y acción robótica.

## Tecnologías utilizadas

- Python
- TensorFlow / Keras
- MobileNetV2
- OpenCV
- NumPy
- Matplotlib
- HDF5 / modelo `.h5`
- Sockets TCP
- NAOqi SDK
- Robot NAO / simulador compatible

## Descripción general

El sistema funciona en dos componentes principales:

1. **Módulo de Machine Learning**
   - Entrena un modelo con imágenes de gestos.
   - Binariza las clases originales en `fist` y `no_fist`.
   - Guarda el modelo entrenado en formato `.h5`.
   - Permite realizar predicción en tiempo real usando cámara.

2. **Módulo de interacción con NAO**
   - Ejecuta un servidor que recibe predicciones.
   - Interpreta mensajes `FIST` o `NO_FIST`.
   - Ejecuta mensajes de voz y movimientos simbólicos del robot.
   - Mantiene postura neutral o postura de alerta según la predicción recibida.

## Estructura del proyecto

```txt
NAO-Fist-Detection-ML/
  README.md
  .gitignore
  requirements.txt
  architecture_diagram.mmd
  video_link.txt

  data/
    README.md
    train/
    validation/
    test/

  docs/
    final_report.pdf
    methodology.md

  models/
    model_fist_detection.h5

  results/
    accuracy_curve.png
    loss_curve.png

  src/
    train_model.py
    predict_and_send.py
    nao_server.py
    nao_movements.py
```

## Archivos principales

### `src/train_model.py`

Script encargado del entrenamiento del modelo.

Incluye:

- Carga del dataset.
- Binarización de clases en `fist` y `no_fist`.
- Aumentación de datos.
- Entrenamiento con MobileNetV2.
- Uso de callbacks como `ModelCheckpoint`, `EarlyStopping` y `ReduceLROnPlateau`.
- Guardado del modelo entrenado.
- Generación de curvas de precisión y pérdida.

### `src/predict_and_send.py`

Script encargado de realizar predicción en tiempo real.

Incluye:

- Carga del modelo entrenado.
- Captura de video con OpenCV.
- Preprocesamiento de frames.
- Predicción `FIST` / `NO_FIST`.
- Envío del resultado al servidor NAO mediante sockets TCP.
- Modo local si no se logra conectar al servidor.

### `src/nao_server.py`

Servidor encargado de recibir predicciones desde el cliente de Machine Learning.

Incluye:

- Recepción de mensajes por socket.
- Interpretación de mensajes `FIST` y `NO_FIST`.
- Integración con NAOqi.
- Ejecución de texto a voz.
- Ejecución de posturas o movimientos simbólicos del robot.

### `src/nao_movements.py`

Script auxiliar con funciones de movimiento y pruebas de interacción con el robot NAO.

Incluye:

- Postura neutral.
- Postura de alerta.
- Movimientos simbólicos.
- Pruebas con cámara y detección de cercanía.

### `models/model_fist_detection.h5`

Modelo entrenado final en formato HDF5.

### `results/`

Contiene las gráficas generadas durante el entrenamiento:

- `accuracy_curve.png`
- `loss_curve.png`

### `data/`

Contiene el dataset utilizado para entrenamiento, validación y prueba.

Para mayor detalle, revisar:

[`data/README.md`](data/README.md)

### `docs/`

Contiene documentación complementaria del proyecto.

- `final_report.pdf`: informe académico final.
- [`methodology.md`](docs/methodology.md): explicación metodológica del flujo de entrenamiento, predicción e integración con NAO.

## Dataset

El dataset está organizado en tres particiones:

```txt
data/
  train/
  validation/
  test/
```

Cada partición contiene subcarpetas correspondientes a clases originales de gestos, por ejemplo:

```txt
fist/
five/
none/
okay/
peace/
rad/
straight/
thumbs/
```

Durante el entrenamiento, estas clases se transforman en un problema binario:

- `fist`: imágenes pertenecientes a la clase puño.
- `no_fist`: imágenes pertenecientes a cualquier otra clase.

Esta transformación permite entrenar un clasificador binario orientado a detectar la presencia del gesto de puño.

## Flujo general del sistema

```txt
Dataset de gestos
  ↓
Binarización fist / no_fist
  ↓
Entrenamiento con MobileNetV2
  ↓
Modelo H5
  ↓
Captura en tiempo real con OpenCV
  ↓
Predicción FIST / NO_FIST
  ↓
Envío por socket TCP
  ↓
Servidor NAO
  ↓
Respuesta verbal y movimiento simbólico
```

## Diagrama de arquitectura

El archivo Mermaid se encuentra en:

```txt
architecture_diagram.mmd
```

Puede visualizarse con herramientas compatibles con Mermaid.

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/Axel-Pariona/NAO-Fist-Detection-ML.git
cd NAO-Fist-Detection-ML
```

Crear un entorno virtual:

```bash
python -m venv .venv
```

Activar el entorno virtual en Windows PowerShell:

```powershell
.venv\Scripts\activate
```

Activar el entorno virtual en Linux o WSL:

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Entrenamiento del modelo

Ejecutar:

```bash
python src/train_model.py
```

El entrenamiento genera o actualiza:

```txt
models/model_fist_detection.h5
results/accuracy_curve.png
results/loss_curve.png
tmp_binarized_dataset/
```

La carpeta `tmp_binarized_dataset/` es generada automáticamente y no debe subirse al repositorio.

## Predicción en tiempo real

Ejecutar:

```bash
python src/predict_and_send.py
```

El script abrirá la cámara, realizará predicciones y mostrará la clasificación en pantalla.

Si el servidor NAO no está disponible, el script puede continuar en modo local.

## Ejecución del servidor NAO

El servidor requiere un entorno compatible con NAOqi.

Configurar variables de entorno según corresponda:

En Windows PowerShell:

```powershell
$env:NAOQI_PATH="C:\ruta\al\pynaoqi\lib"
$env:NAO_IP="127.0.0.1"
$env:NAO_PORT="9559"
$env:SERVER_PORT="5000"
```

En Linux o WSL:

```bash
export NAOQI_PATH="/ruta/al/pynaoqi/lib"
export NAO_IP="127.0.0.1"
export NAO_PORT="9559"
export SERVER_PORT="5000"
```

Ejecutar:

```bash
python src/nao_server.py
```

## Resultados

El proyecto incluye curvas de entrenamiento en la carpeta `results/`.

### Accuracy

```txt
results/accuracy_curve.png
```

### Loss

```txt
results/loss_curve.png
```

Estas figuras permiten revisar la evolución del entrenamiento y validación del modelo.

## Alcance del proyecto

El proyecto corresponde a una práctica académica de Machine Learning con integración robótica.

Incluye:

- Clasificación binaria de imágenes.
- Transfer learning con MobileNetV2.
- Entrenamiento y guardado de modelo.
- Inferencia en tiempo real.
- Comunicación por sockets.
- Respuesta robótica mediante NAOqi.
- Evidencias gráficas del entrenamiento.
- Video de demostración.

## Limitaciones

- El sistema depende de la calidad del dataset y las condiciones de iluminación.
- La predicción puede variar según la cámara, fondo, distancia y postura de la mano.
- La integración con NAO requiere un entorno compatible con NAOqi.
- El servidor NAO puede requerir Python 2.7 según la versión del SDK.
- El modelo fue desarrollado con fines académicos y no está optimizado para producción.
- Los movimientos del robot son simbólicos y controlados.
- La carpeta temporal de binarización se genera en tiempo de entrenamiento.

## Posibles mejoras

- Agregar evaluación sobre el conjunto de prueba.
- Guardar matriz de confusión y reporte de clasificación.
- Exportar métricas en formato CSV.
- Mejorar el preprocesamiento de imágenes.
- Probar arquitecturas más ligeras.
- Implementar detección de mano antes de clasificar.
- Agregar interfaz gráfica de control.
- Mejorar la integración con cámara del robot NAO.
- Crear una versión compatible con TensorFlow Lite.
- Documentar más evidencias visuales del funcionamiento.

## Estado del proyecto

Proyecto académico funcional, reorganizado para presentación en GitHub.

## Autores

- Omar Junior Acuña Villegas
- Axel Yamir Pariona Rojas
- Marcelo Paolo Murguía Lozano
