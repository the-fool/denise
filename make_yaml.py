import sys
import os
import glob
from PIL import Image
import toolz
import random

COLUMNS = 3

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
    #
    # shuffle for looks, so that we don't get a blocky grid
    # we want to leave the "bottom" of the columns where they're at
    # bc they are the smallest images, and shuffling a large image into the end 
    # can potentially cause lopsided columns if the total number of images are not evenly divisible
    min_length = min([len(g) for g in groups])

    for g in groups:
        subset = g[:min_length]
        random.shuffle(subset)
        g[:min_length] = subset
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


if __name__ == '__main__':
    if len(sys.argv) is not 3:
        print("Must give path and title")
        exit()

    path = sys.argv[1]
    title = sys.argv[2]
    yaml = make_yaml(path, title)
    print(yaml)