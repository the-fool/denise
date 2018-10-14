import sys
import os
import glob
from PIL import Image
import toolz
import random

COLUMNS = 3

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
    items.append({
        'rel_height': h / w,
        'yaml': item_string
    })

items_reverse_sorted = sorted(items, key=lambda x: x['rel_height'], reverse=True)
min_group = 0

def sum_group(xs):
    return sum([x['rel_height'] for x in xs])

groups = [list() for _ in range(COLUMNS)]

for i in items_reverse_sorted:
    min_group = groups[0]
    min_sum = sum_group(min_group)

    for g in groups[1:]:
        current_sum = sum_group(g)
        if current_sum <= min_sum:
            min_group = g
    min_group.append(i)

# shuffle for looks, so that we don't get a blocky grid
for g in groups:
    random.shuffle(g)

# now stagger them, so they will be doled out into columns
items = toolz.interleave(groups)

yaml_strings = map(lambda x: x['yaml'], items)

yaml = f"""{yaml}
images:
    {"".join(yaml_strings)}
---
"""

print(yaml)




