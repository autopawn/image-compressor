import argparse
from imgcomp import *

# Using argparse is a good thing :)
ap = argparse.ArgumentParser(description='Compress and decompress images using image compressor')
ap.add_argument("-c",action='store_true',help='Compress mode')
ap.add_argument("-x",action='store_true',help='Decompress mode')
ap.add_argument("input",help='Input file')
ap.add_argument("output",help='Output file')
args = vars(ap.parse_args())

if not (args['c'] or args['x']):
    ap.error('No action requested, add -c or -x')

if args['c']:

    # Load image
    image = load_image(args['input'])
    print("Compressing: %s"%args['input'])
    print("image_shape: %s"%(image.shape,))

    bytes = image_to_bytes(image)
    f = open(args['output'], 'wb')
    f.write(bytes)
    f.close()
