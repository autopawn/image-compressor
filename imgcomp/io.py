import numpy as np

from PIL import Image

def load_image(path):
    # Load image, creates numpy array of uint8
    image = Image.open(path)
    if len(image.getbands())==4:
        image = image.convert('RGBA')
    else:
        image = image.convert('RGB')
    array = np.array(image,dtype='int32')
    return array

def save_image(image,path):
    result = Image.fromarray(image.astype('uint8'))
    result.save(path)
