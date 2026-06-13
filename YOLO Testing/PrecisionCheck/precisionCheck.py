from ultralytics import YOLO

# dein Modell laden
model = YOLO("my_model.pt")

# Evaluation auf VALIDATION SET
#metrics = model.val(data="data.yaml")
metrics = model.val(data="data.yaml")
print(metrics.box.maps)  # pro Klasse mAP