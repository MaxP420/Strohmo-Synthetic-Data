from ultralytics import YOLO

model = YOLO("my_model_backup.pt")

print(model.names)