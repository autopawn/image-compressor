import numpy as np
from .numeric import compress_mat
from .codecs import compress_signed_array

import zlib

def image_to_bytes(img):
    channels = img.shape[2]

    shape = np.array(img.shape,dtype='uint32')
    seq = shape.tobytes()

    for c in range(channels):
        err,bor = compress_mat(img[:,:,c])

        # Get error outliers
        outlier_mask = (np.abs(err)>127)
        err_outliers = err[outlier_mask].astype('int16')

        # Set error values
        # err_c = np.abs(err)
        # err_c = 2*np.abs(err)-(err<0)
        err_c = err+127 # GOOD
        err_c[outlier_mask] = 255
        err_c = err_c.astype('uint8')

        # Compress errors
        # https://docs.python.org/2/library/zlib.html
        compobj = zlib.compressobj(9,zlib.DEFLATED,9,9,zlib.Z_FILTERED)
        err_bytes = compobj.compress(err_c.tobytes())

        # Other bytes
        out_bytes = err_outliers.tobytes()
        bor_bytes = bor.astype('uint8').tobytes()

        # err_compressed = np.zeros((err.size,2),dtype=np.uint8)
        # err_compressed[:,0] = np.abs(err)
        # err_compressed[:,1] = err<0
        # err_compressed = compress_signed_array(err)
        # err_compressed = np.abs(err).astype(dtype=np.uint8).tobytes()
        # err_compressed = err_compressed.T.flatten().tobytes()

        sizes = np.array([len(bor_bytes),len(err_bytes),len(out_bytes)],dtype='uint32')

        seq_c = sizes.tobytes()+bor_bytes+err_bytes+out_bytes
        seq += seq_c

        comp_radio = img[:,:,c].size/len(seq_c)

        print("Channel %d:"%c)
        print("\terr_bytes: %7d"%(len(err_bytes)))
        print("\tout_bytes: %7d"%(len(out_bytes)))
        print("\tbor_bytes: %7d"%(len(bor_bytes)))
        print("\tradio:     %7.4f"%(comp_radio))

        print("\tmean error: %.4f"%(np.mean(np.abs(err))))

    return seq
