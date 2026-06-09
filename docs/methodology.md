# Methodology

Este documento describe la metodología utilizada en el proyecto **NAO Fist Detection ML**, desde la preparación del dataset hasta la integración del modelo con el robot NAO.

## 1. Planteamiento del problema

El proyecto plantea un problema de clasificación de imágenes aplicado a robótica educativa.

La tarea consiste en identificar si una imagen capturada por cámara corresponde a un gesto de puño (`fist`) o a otro tipo de gesto (`no_fist`). El resultado se utiliza para activar una respuesta simbólica del robot NAO.

## 2. Dataset

El dataset contiene imágenes organizadas por clases de gestos de mano.

Clases originales:

- `fist`
- `five`
- `none`
- `okay`
- `peace`
- `rad`
- `straight`
- `thumbs`

La estructura general del dataset es:

```txt
data/
  train/
  validation/
  test/
```

Cada partición mantiene las mismas clases originales.

## 3. Binarización de clases

Aunque el dataset contiene varias clases, el problema se transforma en clasificación binaria:

```txt
fist / no_fist
```

La clase `fist` se conserva como clase positiva. Todas las demás clases se agrupan como `no_fist`.

Esta transformación permite construir un modelo enfocado en detectar únicamente la presencia del gesto de puño.

## 4. Preparación de imágenes

Durante el entrenamiento, las imágenes se redimensionan a:

```txt
160 x 160 píxeles
```

También se aplica normalización de valores de píxel:

```txt
pixel_value / 255.0
```

Esto permite que las imágenes estén en una escala compatible con el modelo de red neuronal.

## 5. Aumentación de datos

Para mejorar la generalización del modelo, se utiliza aumentación de datos sobre el conjunto de entrenamiento.

Entre las transformaciones aplicadas se incluyen:

- Rotación.
- Desplazamiento horizontal.
- Desplazamiento vertical.
- Shear.
- Zoom.
- Volteo horizontal.
- Relleno de píxeles cercanos.

Estas transformaciones ayudan a simular variaciones en posición, orientación y escala de la mano.

## 6. Modelo utilizado

El modelo se basa en **MobileNetV2** mediante transferencia de aprendizaje.

MobileNetV2 se utiliza como extractor de características visuales. Sobre esta base se agregan capas adicionales para la clasificación binaria.

La arquitectura general incluye:

```txt
MobileNetV2 base
  ↓
GlobalAveragePooling2D
  ↓
Dropout
  ↓
Dense
  ↓
Salida binaria
```

## 7. Entrenamiento

El entrenamiento se realiza con Keras y TensorFlow.

Elementos principales del entrenamiento:

- Optimizador Adam.
- Función de pérdida binaria.
- Métrica de accuracy.
- Callbacks para guardar el mejor modelo.
- Reducción de tasa de aprendizaje.
- Detención temprana.

El modelo final se guarda en:

```txt
models/model_fist_detection.h5
```

## 8. Resultados de entrenamiento

Durante el entrenamiento se generan curvas de rendimiento:

```txt
results/accuracy_curve.png
results/loss_curve.png
```

Estas gráficas permiten observar la evolución de la precisión y pérdida durante las épocas de entrenamiento.

## 9. Predicción en tiempo real

El script `src/predict_and_send.py` carga el modelo entrenado y utiliza OpenCV para capturar frames desde una cámara.

Flujo de predicción:

```txt
Frame de cámara
  ↓
Resize a 160x160
  ↓
Normalización
  ↓
Modelo H5
  ↓
Predicción
  ↓
Etiqueta FIST / NO_FIST
```

## 10. Comunicación por sockets

Después de obtener la predicción, el cliente envía el resultado al servidor NAO mediante sockets TCP.

Mensajes utilizados:

```txt
FIST
NO_FIST
```

El envío tiene un tiempo de espera entre mensajes para evitar múltiples activaciones consecutivas.

## 11. Servidor NAO

El archivo `src/nao_server.py` implementa un servidor que recibe mensajes desde el cliente de predicción.

Cuando recibe `FIST`, ejecuta una respuesta de alerta simbólica.

Cuando recibe `NO_FIST`, mantiene o retorna a una postura neutral.

El servidor utiliza NAOqi para:

- Texto a voz.
- Control de postura.
- Movimiento de articulaciones.

## 12. Integración con el robot

La integración final conecta tres componentes:

```txt
Modelo de visión
  ↓
Predicción en tiempo real
  ↓
Servidor NAO
  ↓
Movimiento y voz del robot
```

Esta integración permite demostrar cómo un modelo de Machine Learning puede activar respuestas físicas en un robot humanoide.

## 13. Limitaciones metodológicas

El proyecto tiene algunas limitaciones:

- El modelo depende de las condiciones de iluminación.
- El fondo y la distancia de la cámara pueden afectar la predicción.
- El dataset fue adaptado a una tarea binaria.
- No se incluye una evaluación detallada con matriz de confusión.
- La integración con NAO depende del entorno y versión de NAOqi.
- Los movimientos del robot son demostrativos y controlados.

## 14. Posibles mejoras metodológicas

Se podrían implementar mejoras como:

- Evaluación formal en el conjunto de prueba.
- Matriz de confusión.
- Reporte de precisión, recall y F1-score.
- Detección previa de mano.
- Segmentación de la región de interés.
- Optimización para inferencia en tiempo real.
- Conversión del modelo a TensorFlow Lite.
- Integración directa con cámara del NAO.
- Registro de predicciones en archivo de log.

## Conclusión

La metodología implementada permite construir un flujo completo de Machine Learning aplicado a robótica: entrenamiento del modelo, predicción en tiempo real, comunicación por sockets y respuesta del robot NAO. El proyecto funciona como una demostración académica de integración entre visión por computadora y robótica humanoide.
