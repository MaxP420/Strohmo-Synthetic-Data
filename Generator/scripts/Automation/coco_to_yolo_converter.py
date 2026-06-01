"""Convert COCO annotations to YOLO format JSON"""

import json
import os
import argparse
import uuid


def coco_to_yolo_format(coco_file_path, output_file_path):
    """
    Converts COCO format annotations to YOLO format JSON.
    
    COCO format: bbox = [x, y, width, height] (top-left corner)
    YOLO format: x, y (center), width, height (absolute pixel values)
    
    Args:
        coco_file_path: Path to coco_annotations.json
        output_file_path: Path to save yolo_annotations.json
    """
    
    # Load COCO annotations
    with open(coco_file_path, 'r', encoding='utf-8') as f:
        coco_data = json.load(f)
    
    # Create mapping: category_id -> category_name
    category_map = {}
    for category in coco_data['categories']:
        # Clean class name: remove numeric suffixes like ".001", ".002", etc.
        clean_name = category['name'].split('.')[0]
        category_map[category['id']] = {
            'name': clean_name,
            'id': category['id']
        }
    
    # Create mapping: image_id -> image_name
    image_map = {}
    for image in coco_data['images']:
        image_map[image['id']] = image['file_name']
    
    # Convert annotations to YOLO format
    yolo_annotations = {}
    
    for annotation in coco_data['annotations']:
        image_id = annotation['image_id']
        image_name = image_map[image_id]
        
        # Get category info
        category_id = annotation['category_id']
        category_name = category_map[category_id]['name']
        
        # Convert COCO bbox to YOLO format
        # COCO: [x_min, y_min, width, height]
        # YOLO: center_x, center_y, width, height
        bbox = annotation['bbox']
        x_min = bbox[0]
        y_min = bbox[1]
        width = bbox[2]
        height = bbox[3]
        
        # Calculate center coordinates
        center_x = x_min + width / 2
        center_y = y_min + height / 2
        
        # Create prediction object
        prediction = {
            "x": center_x,
            "y": center_y,
            "width": width,
            "height": height,
            "confidence": 1.0,  # 1.0 for ground truth annotations
            "class": category_name,
            "class_id": category_id,
            "detection_id": str(uuid.uuid4())
        }
        
        # Group by image
        if image_name not in yolo_annotations:
            yolo_annotations[image_name] = {
                "predictions": []
            }
        
        yolo_annotations[image_name]["predictions"].append(prediction)
    
    # Save to JSON file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(yolo_annotations, f, indent=2)
    
    print(f"✅ Conversion complete!")
    print(f"📁 Input: {coco_file_path}")
    print(f"📁 Output: {output_file_path}")
    print(f"📊 Total images: {len(yolo_annotations)}")
    total_predictions = sum(len(img['predictions']) for img in yolo_annotations.values())
    print(f"📊 Total predictions: {total_predictions}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert COCO annotations to YOLO format")
    parser.add_argument('-c', '--coco', dest='coco_file',
                        default='output/coco_data/coco_annotations.json',
                        help='Path to COCO annotations JSON file')
    parser.add_argument('-o', '--output', dest='output_file',
                        default='output/coco_data/yolo_annotations.json',
                        help='Path to save YOLO format JSON file')
    
    args = parser.parse_args()
    
    coco_to_yolo_format(args.coco_file, args.output_file)
