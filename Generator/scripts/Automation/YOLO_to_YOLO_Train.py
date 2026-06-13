import json
from pathlib import Path

# =========================
# CONFIG
# =========================

CLASS_MAP = {
    "blue_cone": 0,
    "yellow_cone": 1,
    "orange_cone": 2,
    "yellow_cone_knocked_over": 3,
    "orange_cone_knocked_over": 3,
    "blue_cone_knocked_over": 3,
    "yellow_cone_damaged": 1,
    "oragnge_cone_damaged": 2,
    "blue_cone_damaged": 0

}

JSON_DIR = Path("D:/Strohmo/Synthetic Data/Strohmo-Synthetic-Data/output/coco_data/yolo_labels")
OUTPUT_DIR = Path("D:/Strohmo/Synthetic Data/Strohmo-Synthetic-Data/YOLO Testing/PrecisionCheck/labels/val")

# =========================
# CONVERTER
# =========================

def convert_box(box, img_w, img_h):
    """
    Converts JSON box to YOLO format
    """

    # JSON format:
    # x, y = center (or top-left depending on dataset!)
    x = box["x"]
    y = box["y"]
    w = box["width"]
    h = box["height"]

    # IMPORTANT: assume x,y = CENTER
    x_center = x / img_w
    y_center = y / img_h
    w_norm = w / img_w
    h_norm = h / img_h

    return x_center, y_center, w_norm, h_norm


def process_file(json_file, output_file):
    with open(json_file, "r") as f:
        data = json.load(f)

    img_w = data["width"]
    img_h = data["height"]

    yolo_lines = []

    for box in data["boxes"]:
        class_name = box["label"]

        if class_name not in CLASS_MAP:
            print(f"Skipping unknown class: {class_name}")
            continue

        class_id = CLASS_MAP[class_name]

        x_center, y_center, w, h = convert_box(box, img_w, img_h)

        yolo_lines.append(
            f"{class_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}"
        )

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w") as f:
        f.write("\n".join(yolo_lines))


def main():
    json_files = list(JSON_DIR.rglob("*.json"))

    print(f"Found {len(json_files)} JSON files")

    for json_file in json_files:

        # same name as image/label
        output_file = OUTPUT_DIR / json_file.with_suffix(".txt").name

        process_file(json_file, output_file)

    print("Conversion done!")


if __name__ == "__main__":
    main()