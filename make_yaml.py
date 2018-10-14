import sys
import os
import glob
from PIL import Image

if len(sys.argv) is not 2:
    print("Must give path")
    exit()

path = sys.argv[1]
yaml = f"""---
image_dir: {path}
"""

items = []

directory = f'static/img/{path}'

for img_fname in os.listdir(directory):
    i = Image.open(f'{directory}/{img_fname}')
    w, h = i.size
    item_string = f"""- name: {img_fname}
      width: {w}
      height: {h}
      caption:
      description:

    """
    items.append(item_string)

yaml = f"""{yaml}
image_dir: {path}
images:
    {"".join(items)}
---
"""

print(yaml)




