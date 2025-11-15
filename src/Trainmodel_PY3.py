# train_fist_model.py
# Python 3
# Entrena un clasificador binario (fist / no_fist) usando MobileNetV2 (transfer learning).
# Ajusta DATA_DIR y EPOCHS abajo si lo deseas.

import os
import json
import shutil
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping

# ----------------- CONFIG -----------------
DATA_DIR = "C:\\Users\\Lenovo\\Downloads\\PC3-ML\\DATASET\\data"     # debe contener 'train' y opcionalmente 'valid'; si no hay 'valid' usará validation_split
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VALID_DIR = os.path.join(DATA_DIR, "valid")  # opcional
IMG_SIZE = (160, 160)
BATCH_SIZE = 32
EPOCHS = 10            # <-- Cambia aquí si quieres otro número de épocas (actualmente 10)
OUTPUT_MODEL = "model_fist_detection.h5"
LABEL_MAP_OUT = "label_map.json"
LEARNING_RATE = 1e-4
# ------------------------------------------

# Crear una carpeta temporal para binarizar clases si es necesario:
# Queremos que en train/ exista "fist" y "no_fist"
def ensure_binary_structure(orig_train_dir, temp_train_dir):
    """
    Crea estructura temp_train_dir/train/fist y temp_train_dir/train/no_fist copiando las imágenes
    desde orig_train_dir que contiene subfolders como 'fist', 'five', 'peace', etc.
    """
    if os.path.exists(temp_train_dir):
        shutil.rmtree(temp_train_dir)
    os.makedirs(os.path.join(temp_train_dir, "train", "fist"))
    os.makedirs(os.path.join(temp_train_dir, "train", "no_fist"))
    for sub in os.listdir(orig_train_dir):
        subpath = os.path.join(orig_train_dir, sub)
        if not os.path.isdir(subpath):
            continue
        if sub.lower() == "fist":
            dst = os.path.join(temp_train_dir, "train", "fist")
        else:
            dst = os.path.join(temp_train_dir, "train", "no_fist")
        for f in os.listdir(subpath):
            if f.lower().endswith(('.png','.jpg','.jpeg','.bmp')):
                try:
                    shutil.copy(os.path.join(subpath, f), dst)
                except Exception:
                    pass

# Si VALID_DIR existe, lo binarizamos también
def ensure_binary_valid_structure(orig_valid_dir, temp_dir):
    os.makedirs(os.path.join(temp_dir, "valid", "fist"))
    os.makedirs(os.path.join(temp_dir, "valid", "no_fist"))
    for sub in os.listdir(orig_valid_dir):
        subpath = os.path.join(orig_valid_dir, sub)
        if not os.path.isdir(subpath):
            continue
        if sub.lower() == "fist":
            dst = os.path.join(temp_dir, "valid", "fist")
        else:
            dst = os.path.join(temp_dir, "valid", "no_fist")
        for f in os.listdir(subpath):
            if f.lower().endswith(('.png','.jpg','.jpeg','.bmp')):
                try:
                    shutil.copy(os.path.join(subpath, f), dst)
                except Exception:
                    pass

# Preparar datos
temp_dir = "tmp_binarized_dataset"
if not os.path.exists(TRAIN_DIR):
    raise SystemExit("No se encontró carpeta TRAIN: {}".format(TRAIN_DIR))

print("Preparando dataset binario en:", temp_dir)
ensure_binary_structure(TRAIN_DIR, temp_dir)
if os.path.exists(VALID_DIR):
    ensure_binary_valid_structure(VALID_DIR, temp_dir)
    use_valid = True
else:
    use_valid = False

train_dir_final = os.path.join(temp_dir, "train")
valid_dir_final = os.path.join(temp_dir, "valid") if use_valid else None

# Generadores
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=12,
    width_shift_range=0.08,
    height_shift_range=0.08,
    shear_range=0.08,
    zoom_range=0.08,
    horizontal_flip=True,
    fill_mode="nearest",
    validation_split=0.15 if not use_valid else 0.0  # si no hay valid, separamos parte de train
)

if use_valid:
    valid_datagen = ImageDataGenerator(rescale=1./255)
    train_flow = train_datagen.flow_from_directory(train_dir_final,
                                                   target_size=IMG_SIZE,
                                                   batch_size=BATCH_SIZE,
                                                   class_mode="binary",
                                                   shuffle=True)
    valid_flow = valid_datagen.flow_from_directory(valid_dir_final,
                                                   target_size=IMG_SIZE,
                                                   batch_size=BATCH_SIZE,
                                                   class_mode="binary",
                                                   shuffle=False)
else:
    train_flow = train_datagen.flow_from_directory(train_dir_final,
                                                   target_size=IMG_SIZE,
                                                   batch_size=BATCH_SIZE,
                                                   class_mode="binary",
                                                   shuffle=True,
                                                   subset='training')
    valid_flow = train_datagen.flow_from_directory(train_dir_final,
                                                   target_size=IMG_SIZE,
                                                   batch_size=BATCH_SIZE,
                                                   class_mode="binary",
                                                   shuffle=False,
                                                   subset='validation')

# Guardar map de etiquetas (por si acaso)
label_map = {v:k for k,v in train_flow.class_indices.items()}  # e.g. {0:'fist', 1:'no_fist'}
with open(LABEL_MAP_OUT, "w") as f:
    json.dump(label_map, f)
print("Label map guardado:", label_map)

# Modelo (transfer learning)
base = MobileNetV2(input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
                   include_top=False, weights="imagenet")
base.trainable = False

x = base.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3)(x)
x = Dense(64, activation="relu")(x)
x = Dropout(0.25)(x)
preds = Dense(1, activation="sigmoid")(x)

model = Model(inputs=base.input, outputs=preds)
model.compile(optimizer=Adam(learning_rate=LEARNING_RATE),
              loss="binary_crossentropy",
              metrics=["accuracy"])

print(model.summary())

# Callbacks
mc = ModelCheckpoint(OUTPUT_MODEL, monitor="val_accuracy", save_best_only=True, verbose=1)
rl = ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3, verbose=1)
es = EarlyStopping(monitor="val_loss", patience=6, restore_best_weights=True, verbose=1)

history = model.fit(
    train_flow,
    epochs=EPOCHS,
    validation_data=valid_flow,
    callbacks=[mc, rl, es]
)

# Evaluación final
loss, acc = model.evaluate(valid_flow)
print("Validation loss: {:.4f}, acc: {:.4f}".format(loss, acc))

model.save(OUTPUT_MODEL)
print("Modelo guardado en:", OUTPUT_MODEL)

# Guardar curvas (opcionales)
try:
    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(history.history['accuracy'], label='train_acc')
    plt.plot(history.history['val_accuracy'], label='val_acc')
    plt.legend()
    plt.title("Accuracy")
    plt.savefig("accuracy_curve.png")

    plt.figure()
    plt.plot(history.history['loss'], label='train_loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.legend()
    plt.title("Loss")
    plt.savefig("loss_curve.png")
    print("Curvas guardadas.")
except Exception as e:
    print("No se pudieron guardar curvas:", e)

# limpiar temp si quieres (opcional)
# shutil.rmtree(temp_dir)
print("Entrenamiento completado.")
