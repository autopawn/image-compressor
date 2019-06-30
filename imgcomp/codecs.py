import numpy as np
import pyfastpfor

# Print available codecs
# print(pyfastpfor.getCodecList())
# ['BP32', 'copy', 'fastbinarypacking16', 'fastbinarypacking32',
#   'fastbinarypacking8', 'fastpfor128', 'fastpfor256', 'maskedvbyte',
#   'newpfor', 'optpfor', 'pfor', 'pfor2008', 'simdbinarypacking',
#   'simdfastpfor128', 'simdfastpfor256', 'simdgroupsimple',
#   'simdgroupsimple_ringbuf', 'simdnewpfor', 'simdoptpfor', 'simdpfor',
#   'simdsimplepfor', 'simple16', 'simple8b', 'simple8b_rle', 'simple9',
#   'simple9_rle', 'simplepfor', 'streamvbyte', 'varint', 'varintg8iu',
#   'varintgb', 'vbyte', 'vsencoding']

CODEC = "simdfastpfor256"

def compress_signed_array(arr):

    arr = (2*np.abs(arr)-(arr<0)).astype(np.uint32)

    out_arr = np.zeros(arr.size*2+32,dtype=np.uint32)

    codec = pyfastpfor.getCodec(CODEC)
    len = codec.encodeArray(arr,arr.size,out_arr,out_arr.size)
    out_arr = out_arr[:len]

    return out_arr

def decompress_signed_array(arr,len):
    codec = pyfastpfor.getCodec(CODEC)

    dec_arr = np.zeros(len,dtype=np.uint32)
    len = codec.decodeArray(arr,arr.size,dec_arr,len)

    # FIXME: not right:
    dec_arr = (dec_arr.astype(np.int32)//2)*(1-2*(dec_arr%2))

    return dec_arr
