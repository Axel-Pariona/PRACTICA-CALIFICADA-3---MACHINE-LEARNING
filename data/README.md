# Dataset

Esta carpeta contiene el dataset utilizado para entrenar, validar y probar el modelo de detección de gesto de puño del proyecto **NAO Fist Detection ML**.

## Estructura

El dataset está organizado en tres particiones:

```txt
data/
  train/
  validation/
  test/
```

Cada partición contiene subcarpetas con las clases originales de gestos:

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

## Clases originales

Las clases representan distintos gestos de mano:

- `fist`: gesto de puño.
- `five`: mano abierta.
- `none`: ausencia de gesto específico.
- `okay`: gesto de OK.
- `peace`: gesto de paz.
- `rad`: gesto alternativo de mano.
- `straight`: mano recta.
- `thumbs`: pulgar arriba.

## Conversión a clasificación binaria

Aunque el dataset contiene múltiples clases, el proyecto se enfoca en una clasificación binaria:

```txt
fist
no_fist
```

Durante el entrenamiento, el script `src/train_model.py` convierte temporalmente las clases originales de la siguiente manera:

| Clase original | Clase binaria |
|---|---|
| `fist` | `fist` |
| `five` | `no_fist` |
| `none` | `no_fist` |
| `okay` | `no_fist` |
| `peace` | `no_fist` |
| `rad` | `no_fist` |
| `straight` | `no_fist` |
| `thumbs` | `no_fist` |

Esta conversión se realiza en una carpeta temporal llamada:

```txt
tmp_binarized_dataset/
```

Dicha carpeta se genera automáticamente y no debe subirse al repositorio.

## Uso dentro del proyecto

El dataset se utiliza en:

```txt
src/train_model.py
```

El script espera la siguiente estructura:

```txt
data/
  train/
    fist/
    five/
    none/
    okay/
    peace/
    rad/
    straight/
    thumbs/

  validation/
    fist/
    five/
    none/
    okay/
    peace/
    rad/
    straight/
    thumbs/

  test/
    fist/
    five/
    none/
    okay/
    peace/
    rad/
    straight/
    thumbs/
```

## Entrenamiento

Para entrenar el modelo usando este dataset:

```bash
python src/train_model.py
```

El script realiza:

1. Lectura de imágenes.
2. Conversión temporal a clases `fist` y `no_fist`.
3. Preprocesamiento y aumentación de datos.
4. Entrenamiento con MobileNetV2.
5. Guardado del modelo en `models/`.
6. Generación de curvas en `results/`.

## Consideraciones

- El dataset se conserva en el repositorio porque su tamaño es manejable para este proyecto académico.
- Si el dataset crece demasiado, se recomienda moverlo a almacenamiento externo y documentar el enlace.
- La carpeta `tmp_binarized_dataset/` no debe versionarse porque puede regenerarse.
- Las imágenes deben mantenerse organizadas por clase para que `ImageDataGenerator` pueda leerlas correctamente.

## Nota

Este dataset fue utilizado con fines académicos para entrenar un clasificador binario de gestos de mano e integrarlo con una demostración robótica usando NAO.
