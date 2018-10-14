import sys
import os
import glob
from PIL import Image
import toolz
import random

COLUMNS = 3

if __name__ == '__main__':
    if len(sys.argv) is not 2:
        print("Must give path")
        exit()

    path = sys.argv[1]
    yaml = make_yaml(path)
    print(yaml)

def make_yaml(path, title=None):
    yaml = f"""---
    title: {title}
    image_dir: {path}
    """

    items = []

    directory = f'static/img/{path}'

    for img_fname in os.listdir(directory):
        i = Image.open(f'{directory}/{img_fname}')
        w, h = i.size
        item_string = f"""
        - name: {img_fname}
          width: {w}
          height: {h}
          caption:
          description:

        """

        # displaying in a column on the page, the apparent height is relative to width
        items.append({
            'rel_height': h / w,
            'yaml': item_string
        })


    #
    # Need to balance out the columns of images for the gallery
    # The columns are templated according to the modulus of the index of the item in a list
    # so, the kth column will include every image whose index % k == 0
    #

    #
    # In order for a good even bucketing, start with a *reverse* sorted array
    #
    items_reverse_sorted = sorted(
        items, key=lambda x: x['rel_height'], reverse=True)

    # utility function
    def sum_group(xs):
        return sum([x['rel_height'] for x in xs])

    groups = [list() for _ in range(COLUMNS)]

    for item in items_reverse_sorted:
        min_group = groups[0]
        min_sum = sum_group(min_group)

        for g in groups:
            current_sum = sum_group(g)
            if current_sum < min_sum:
                min_group = g
        min_group.append(item)

    # shuffle for looks, so that we don't get a blocky grid
    for g in groups:
        random.shuffle(g)
    random.shuffle(groups)

    # now stagger them, so they will be doled out into columns
    items = toolz.interleave(groups)

    # finally, cook up the yaml
    yaml_strings = map(lambda x: x['yaml'], items)

    yaml = f"""{yaml}
    images:
        {"".join(yaml_strings)}
---
    """

    return yaml
