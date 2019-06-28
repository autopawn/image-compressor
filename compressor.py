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
    image = load_image(args['input'])
    target_shape = image.shape

    pred = RegularInterpolator()
    err,bor = compress_mat(pred,image[:,:,0])
    print(err)
    print(bor)
    print(np.mean(np.abs(err)))

    print("target_shape: %s"%(target_shape,))
