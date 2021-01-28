import os
from PIL import Image

def get_name(filename):
    return os.path.splitext(filename)[0];

def get_extension(filename):
    return os.path.splitext(filename)[1];

def image_optimization(path, cover=False):
    img = Image.open(path);

    if cover:
        img.resize((243, 300), Image.ANTIALIAS);

    img.save(path, optimize=True, quality=95);
