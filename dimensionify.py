from PIL import Image
import glob
import os
import re

for fname in glob.iglob('static/img/*.jpg'):
    already_done = bool(re.search('\d+x\d+', fname))
    print(fname)
    if already_done:
        continue
    # urlify = lambda n: f'static/img/{n}'
    i = Image.open(fname)
    w, h = i.size
    base_fname, extension = fname.split('.')
    new_fname = f'{base_fname}_{w}x{h}.{extension}'
    os.rename(fname, new_fname)

