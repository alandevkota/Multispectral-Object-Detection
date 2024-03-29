import os
import json
import xml.etree.ElementTree as ET
from typing import List, Dict

def get_annotations(xml_path: str) -> List[Dict]:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    annotations = []
    for obj in root.iter('object'):
        name = obj.find('name').text
        bbox = obj.find('bndbox')
        x_elem = bbox.find('x')
        y_elem = bbox.find('y')
        w_elem = bbox.find('w')
        h_elem = bbox.find('h')
        if x_elem is not None and y_elem is not None and w_elem is not None and h_elem is not None:
            x = int(x_elem.text)
            y = int(y_elem.text)
            w = int(w_elem.text)
            h = int(h_elem.text)
            annotations.append({
                'name': name,
                'bbox': [x, y, w, h]
            })
    return annotations


def convert_to_coco(xml_dir: str, output_json: str):
    data_dict = {}
    data_dict['images'] = []
    data_dict['annotations'] = []
    data_dict['categories'] = [{'id': 1, 'name': 'person'}, {'id': 2, 'name': 'people'}, {'id': 3, 'name': 'cyclist'}]
    annotation_id = 0
    for i, xml_file in enumerate(os.listdir(xml_dir)):
        if not xml_file.endswith('.xml'):
            continue
        xml_path = os.path.join(xml_dir, xml_file)
        annotations = get_annotations(xml_path)
        image_id = i + 1
        data_dict['images'].append({'id': image_id, 'file_name': xml_file.replace('.xml', '.jpg')})
        for annotation in annotations:
            if annotation['name'] == 'person':
                category_id = 1
            elif annotation['name'] == 'people':
                category_id = 2
            elif annotation['name'] == 'cyclist':
                category_id = 3
            else:
                continue  # skip annotations with other names
            data_dict['annotations'].append({
                'id': annotation_id,
                'image_id': image_id,
                'category_id': category_id,
                'bbox': annotation['bbox'],
                'area': annotation['bbox'][2] * annotation['bbox'][3],
                'iscrowd': 0
            })
            annotation_id += 1
    with open(output_json, 'w') as f:
        json.dump(data_dict, f)

# usage
# convert_to_coco('C:/Users/aland/Desktop/Kaist_Small/annotations/set05/V000', 'C:/Users/aland/Desktop/Kaist_Small/images/set05/V000/visible/_annotations.coco.json')
convert_to_coco('C:/Users/aland/Desktop/Kaist_Small/annotations/set05/V000', 'C:/Users/aland/Desktop/Kaist_Small/images/set05/V000/lwir/_annotations.coco.json')