import numpy as np
from .numeric import compress_mat,decompress_mat
from .codecs import compress_signed_array

import zlib

def image_to_bytes(img):
    channels = img.shape[2]

    shape = np.array(img.shape,dtype='uint32')
    seq = shape.tobytes()

    for c in range(channels):

        print("Channel %d:"%c)

        err,bor = compress_mat(img[:,:,c])

        print("\tmean error:%9.4f"%(np.mean(np.abs(err))))

        # Get error outliers
        outlier_mask = (np.abs(err)>127)
        err_outliers = err[outlier_mask].astype('int16')

        # Set error values
        err_c = err+127
        err_c[outlier_mask] = 255
        err_c = err_c.astype('uint8')

        # Compress errors
        # https://docs.python.org/2/library/zlib.html
        err_bytes = zlib.compress(err_c.tobytes(),9)

        # Other bytes
        out_bytes = err_outliers.tobytes()
        bor_bytes = bor.astype('uint8').tobytes()

        sizes = np.array([len(bor_bytes),len(err_bytes),len(out_bytes)],dtype='uint32')

        seq_c = sizes.tobytes()+bor_bytes+err_bytes+out_bytes
        seq += seq_c

        comp_radio = img[:,:,c].size/len(seq_c)

        print("\terr_bytes: %9d"%(len(err_bytes)))
        print("\tout_bytes: %9d"%(len(out_bytes)))
        print("\tbor_bytes: %9d"%(len(bor_bytes)))
        print("\tradio:     %9.4f"%(comp_radio))

    f_radio = img.size/float(len(seq))
    print("Final radio: %9.4f"%(f_radio))

    return seq

def bytes_to_image(bytes):
    # Read shape
    offset = 0
    shape = np.frombuffer(bytes,dtype='uint32',count=3,offset=offset)
    offset += 3*4
    image = np.zeros(shape,dtype='uint8')

    channels = shape[2]
    for c in range(channels):
        print("Reading channel %d"%c)
        sizes = np.frombuffer(bytes,dtype='uint32',count=3,offset=offset)
        offset += 3*4

        borders = np.frombuffer(bytes,dtype='uint8',count=sizes[0],offset=offset)
        offset += sizes[0]

        errors_c = bytes[offset:offset+sizes[1]]
        offset += sizes[1]

        outliers = np.frombuffer(bytes,dtype='int16',count=sizes[2]//2,offset=offset)
        offset += sizes[2]

        # Reconstruct errors
        error_buff = zlib.decompress(errors_c)
        errors = np.frombuffer(error_buff,dtype='uint8',count=len(error_buff),offset=0)
        errors = errors.astype('int32')
        outlier_mask = (errors==255)
        errors -= 127
        errors[outlier_mask] = outliers

        # Get channel matrix
        image[:,:,c] = decompress_mat(shape[:2],errors,borders)

    return image
