"""Convert COCO annotations to YOLO format with separate JSON per image"""

import json
import os
import argparse
from pathlib import Path


def coco_to_yolo_per_image(coco_file_path, output_dir):
    """
    Converts COCO format annotations to YOLO format JSON with one file per image.
    
    COCO format: bbox = [x, y, width, height] (top-left corner)
    YOLO format: x, y (center), width, height (absolute pixel values)
    
    Args:
        coco_file_path: Path to coco_annotations.json
        output_dir: Directory to save individual YOLO JSON files
    """
    
    # Load COCO annotations
    with open(coco_file_path, 'r', encoding='utf-8') as f:
        coco_data = json.load(f)
    
    # Create mapping: category_id -> category_name (clean names)
    category_map = {}
    for category in coco_data['categories']:
        # Clean class name: remove numeric suffixes like ".001", ".002", etc.
        clean_name = category['name'].split('.')[0]
        category_map[category['id']] = clean_name
    
    # Create mapping: image_id -> image info
    image_map = {}
    for image in coco_data['images']:
        image_map[image['id']] = {
            'file_name': image['file_name'],
            'width': image['width'],
            'height': image['height']
        }
    
    # Group annotations by image_id
    annotations_by_image = {}
    for annotation in coco_data['annotations']:
        image_id = annotation['image_id']
        if image_id not in annotations_by_image:
            annotations_by_image[image_id] = []
        annotations_by_image[image_id].append(annotation)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate YOLO JSON for each image
    count = 0
    for image_id, annotations in annotations_by_image.items():
        image_info = image_map[image_id]
        image_name = image_info['file_name']
        width = image_info['width']
        height = image_info['height']
        
        # Create boxes array
        boxes = []
        for annotation in annotations:
            category_id = annotation['category_id']
            label = category_map[category_id]
            
            # Convert COCO bbox to YOLO format
            # COCO: [x_min, y_min, width, height]
            # YOLO: center_x, center_y, width, height
            bbox = annotation['bbox']
            x_min = bbox[0]
            y_min = bbox[1]
            box_width = bbox[2]
            box_height = bbox[3]
            
            # Calculate center coordinates
            center_x = x_min + box_width / 2
            center_y = y_min + box_height / 2
            
            box_obj = {
                "label": label,
                "x": center_x,
                "y": center_y,
                "width": box_width,
                "height": box_height,
                "keypoints": None
            }
            boxes.append(box_obj)
        
        # Create YOLO annotation object
        yolo_annotation = {
            "boxes": boxes,
            "height": height,
            "key": image_name,
            "width": width
        }
        
        # Generate output filename (replace .jpg with .json)
        base_name = Path(image_name).stem
        output_filename = f"{base_name}.json"
        output_path = os.path.join(output_dir, output_filename)
        
        # Save to JSON file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(yolo_annotation, f, indent=2)
        
        count += 1
    
    print(f"✅ Conversion complete!")
    print(f"📁 Input: {coco_file_path}")
    print(f"📁 Output directory: {output_dir}")
    print(f"📊 Total images processed: {count}")
    total_annotations = sum(len(annotations) for annotations in annotations_by_image.values())
    print(f"📊 Total annotations: {total_annotations}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert COCO annotations to YOLO format (one JSON per image)")
    parser.add_argument('-c', '--coco', dest='coco_file',
                        default='output/coco_data/coco_annotations.json',
                        help='Path to COCO annotations JSON file')
    parser.add_argument('-o', '--output', dest='output_dir',
                        default='output/coco_data/yolo_labels',
                        help='Directory to save YOLO format JSON files')
    
    args = parser.parse_args()
    
    coco_to_yolo_per_image(args.coco_file, args.output_dir)
