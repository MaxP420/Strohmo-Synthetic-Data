from ultralytics import YOLO

# Modell laden
model = YOLO("my_model.pt")



# Auf kompletten Bilderordner anwenden
results = model.predict(
    source="bild",
    save=True,
    conf=0.25
)

print("Fertig!")