from ultralytics import YOLO

model = YOLO("my_model.pt")

model.model.names = {
    0: "blue_cone",
    1: "yellow_cone",
    2: "orange_cone",
    3: "knocked_over"
}

model.save("my_model.pt")