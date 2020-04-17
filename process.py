import glob
import xmltodict
import json
import shutil
from os.path import basename

traintxt = open('data/captcha/train.txt', 'w', encoding='utf-8')
label = open('data/captcha/labels/train.txt', 'w', encoding='utf-8')

for file in glob.glob('data/raw/*.xml'):
    print('file', file)
    
    xml_str = open(file, encoding='utf-8').read()
    data = xmltodict.parse(xml_str)
    data = json.loads(json.dumps(data))
    print('data', json.dumps(data, indent=2))
    
    annoatation = data.get('annotation')
    print('anno', annoatation)
    
    image = annoatation.get('path')
    
    shutil.copy(image, f'./data/captcha/images/{basename(image)}')
    
    width = int(annoatation.get('size').get('width'))
    height = int(annoatation.get('size').get('height'))
    
    bndbox = annoatation.get('object').get('bndbox')
    xmin = int(bndbox.get('xmin'))
    xmax = int(bndbox.get('xmax'))
    ymin = int(bndbox.get('ymin'))
    ymax = int(bndbox.get('ymax'))
    
    center_x = ((xmin + xmax) / 2) / width
    center_y = ((ymin + ymax) / 2) / height
    
    width = (xmax - xmin) / width
    height = (ymax - ymin) / height
    
    print('center x', center_x)
    print('center y', center_y)
    print('width', width)
    print('height', height)

    traintxt.write(f'data/captcha/images/{basename(image)}\n')
    label.write(f'0 {center_x} {center_y} {width} {height}\n')
    
    # break
