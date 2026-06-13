from ultralytics import YOLO
from pathlib import Path
import cv2
import numpy as np
import pandas as pd

# ============================================================
# YOLO Object Detection Auswertung
# Für normales Object-Detection-Modell, KEIN Segmentierungsmodell
# ============================================================

MODEL_PATH = "yolov26n640.pt"
IMAGE_DIR = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\YOLO Testing\\PrecisionCheck\\images\\val"          # Ordner mit deinen Bildern
OUTPUT_DIR = "outputs"

# Sehr niedrige Schwelle:
# YOLO erlaubt technisch nicht "gar keine" Schwelle,
# aber 0.001 nimmt praktisch alles mit.
CONF_THRESHOLD = 0.001

# NMS-Einstellung:
# agnostic_nms=True verhindert, dass derselbe Kegel gleichzeitig
# als mehrere Klassen behalten wird.
IOU_THRESHOLD = 0.7
MAX_DET = 300

# ============================================================
# Modell laden
# ============================================================

model = YOLO(MODEL_PATH)

image_dir = Path(IMAGE_DIR)
output_dir = Path(OUTPUT_DIR)

annotated_dir = output_dir / "annotated_images"
matrix_dir = output_dir / "object_matrices_csv"
summary_dir = output_dir / "summary"

annotated_dir.mkdir(parents=True, exist_ok=True)
matrix_dir.mkdir(parents=True, exist_ok=True)
summary_dir.mkdir(parents=True, exist_ok=True)

image_paths = []
for ext in ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.webp"]:
    image_paths.extend(image_dir.glob(ext))

print(f"{len(image_paths)} Bilder gefunden.")

all_detections = []

# ============================================================
# Bilder auswerten
# ============================================================

for image_path in image_paths:
    print(f"Verarbeite: {image_path.name}")

    img = cv2.imread(str(image_path))
    if img is None:
        print(f"Warnung: Bild konnte nicht gelesen werden: {image_path}")
        continue

    h, w = img.shape[:2]

    results = model.predict(
        source=str(image_path),
        conf=CONF_THRESHOLD,
        iou=IOU_THRESHOLD,
        agnostic_nms=True,
        max_det=MAX_DET,
        verbose=False
    )

    result = results[0]

    detections = []

    if result.boxes is not None and len(result.boxes) > 0:
        boxes = result.boxes.xyxy.cpu().numpy()
        confs = result.boxes.conf.cpu().numpy()
        classes = result.boxes.cls.cpu().numpy().astype(int)

        for object_id, (box, conf, cls_id) in enumerate(zip(boxes, confs, classes)):
            x1, y1, x2, y2 = box

            # Werte auf Bildgrenzen begrenzen
            x1 = max(0, min(float(x1), w - 1))
            y1 = max(0, min(float(y1), h - 1))
            x2 = max(0, min(float(x2), w - 1))
            y2 = max(0, min(float(y2), h - 1))

            class_name = model.names[int(cls_id)]

            row = {
                "image": image_path.name,
                "image_width": w,
                "image_height": h,
                "object_id": object_id,

                # Nur eine Klasse pro erkanntem Objekt:
                # YOLO liefert hier bereits die wahrscheinlichste Klasse für diese Box.
                "class_id": int(cls_id),
                "class_name": class_name,
                "confidence": float(conf),

                # Bounding Box
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,

                # Mittelpunkt und Größe
                "center_x": float((x1 + x2) / 2),
                "center_y": float((y1 + y2) / 2),
                "box_width": float(x2 - x1),
                "box_height": float(y2 - y1),
                "box_area": float((x2 - x1) * (y2 - y1)),

                # Normalisierte Werte zwischen 0 und 1
                "x1_norm": x1 / w,
                "y1_norm": y1 / h,
                "x2_norm": x2 / w,
                "y2_norm": y2 / h,
                "center_x_norm": ((x1 + x2) / 2) / w,
                "center_y_norm": ((y1 + y2) / 2) / h,
                "box_width_norm": (x2 - x1) / w,
                "box_height_norm": (y2 - y1) / h,
            }

            detections.append(row)
            all_detections.append(row)

    # ========================================================
    # Objekt-Matrix pro Bild speichern
    # ========================================================
    # Diese CSV ist deine "Matrix":
    # Jede Zeile = ein erkannter Kegel / ein erkanntes Objekt.
    # Jede Zeile hat genau eine Klasse, nämlich die Klasse mit der
    # höchsten Wahrscheinlichkeit für diese Box.
    # ========================================================

    df = pd.DataFrame(detections)
    csv_path = matrix_dir / f"{image_path.stem}_object_matrix.csv"
    df.to_csv(csv_path, index=False)

    # ========================================================
    # Diagramm / annotiertes Bild speichern
    # ========================================================

    annotated = result.plot()
    annotated_path = annotated_dir / f"{image_path.stem}_detections.jpg"
    cv2.imwrite(str(annotated_path), annotated)

# ============================================================
# Gesamtübersicht speichern
# ============================================================

all_df = pd.DataFrame(all_detections)
all_csv_path = summary_dir / "all_detections_matrix.csv"
all_df.to_csv(all_csv_path, index=False)

if len(all_df) > 0:
    count_summary = (
        all_df
        .groupby(["image", "class_name"])
        .size()
        .reset_index(name="count")
    )
else:
    count_summary = pd.DataFrame(columns=["image", "class_name", "count"])

count_summary_path = summary_dir / "count_summary_per_image.csv"
count_summary.to_csv(count_summary_path, index=False)

print("Fertig.")
print(f"Annotierte Bilder: {annotated_dir}")
print(f"Objekt-Matrizen pro Bild: {matrix_dir}")
print(f"Gesamtmatrix: {all_csv_path}")
print(f"Zählübersicht: {count_summary_path}")
