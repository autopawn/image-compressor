import numpy as np
from .numeric import compress_mat
from .codecs import compress_signed_array

def image_to_bytes(img):
    channels = img.shape[2]

    shape = np.array(img.shape,dtype='uint32')
    seq = shape.tobytes()

    for c in range(channels):
        err,bor = compress_mat(img[:,:,c])
        err_compressed = compress_signed_array(err)

        sizes = np.array([bor.size,4*err_compressed.size],dtype='uint32')

        seq += sizes.tobytes()+bor.tobytes()+err_compressed.tobytes()

        err_bytes = 4*err_compressed.size
        bor_bytes = bor.size
        comp_radio = img[:,:,c].size/float(err_bytes+bor_bytes)

        print("Channel %d:"%c)
        print("\terr_bytes: %6d"%(err_bytes))
        print("\tbor_bytes: %6d"%(bor_bytes))
        print("\tradio:      %.4f"%(comp_radio))

        print("\tmean error: %.4f"%(np.mean(np.abs(err))))

    return seq
