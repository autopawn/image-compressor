import os
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
    ap.error('No action requested, add -c or -x.')

if (args['c'] and args['x']):
    ap.error('More than one action requested.')

if args['c']:
    # Load image
    assert(args['input'])
    image = load_image(args['input'])
    print("Compressing: %s"%args['input'])
    print("image_shape: %s"%(image.shape,))

    print("Saving to \"%s\""%args['output'])
    bytes = image_to_bytes(image)
    f = open(args['output'], 'wb')
    f.write(bytes)
    f.close()

elif args['x']:
    name, extension = os.path.splitext(args['output'])
    assert(extension=='.png')
    # Load bin
    input_file = open(args['input'],"rb")
    data = input_file.read()
    input_file.close()

    image = bytes_to_image(data)

    print("Saving to \"%s\""%args['output'])
    save_image(image,args['output'])
