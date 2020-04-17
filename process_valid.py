import glob
import xmltodict
import json
import shutil
from os.path import basename

traintxt = open('data/captcha/valid.txt', 'w', encoding='utf-8')
label = open('data/captcha/labels/valid.txt', 'w', encoding='utf-8')

for file in glob.glob('data/raw/valid/*.xml'):
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
    # label.write(f'0 {round(center_x, 8)} {round(center_y, 8)} {round(width, 8)} {round(height, 8)}\n')

    with open(f'data/captcha/labels/{basename(image).replace(".png", ".txt")}', 'w', encoding='utf-8') as f:
        f.write(f'0 {round(center_x, 8)} {round(center_y, 8)} {round(width, 8)} {round(height, 8)}\n')

    # break
