from numba import jit
import numpy as np

from .predictors import *

from .utils import *

@jit('int32[:](int32[:,:],int32[:,:])',nopython=True)
def get_errors(prev,mat):
    errors = np.zeros(mat.shape[0]*mat.shape[1]*3//4,dtype=np.int32)

    # Extended prev matrix
    etprev = extend(prev)

    # Image currently known on hipothetical decompression
    etknown = scale2x(etprev)

    # Predict pixels (could be done in diagonal, in parallel)
    i = 0
    for y in range(mat.shape[0]//2):
        for x in range(mat.shape[1]//2):
            # Get red window
            red = etprev[y:y+3,x:x+3]
            # Get blue window
            blue = etknown[2*y:2*y+4,2*x:2*x+4]
            # Get predictions
            nw,ne,sw = predict(red,blue)
            # Get errors
            err_nw = nw-mat[2*y,2*x]
            err_ne = ne-mat[2*y,2*x+1]
            err_sw = sw-mat[2*y+1,2*x]
            # if x==mat.shape[1]//4:
            #     print("%3d %3d %3d -> %+4d %+4d %+4d"%(nw,ne,sw,err_nw,err_ne,err_sw))

            # Update errors
            errors[i+0] = err_nw;
            errors[i+1] = err_ne;
            errors[i+2] = err_sw;
            i += 3

            # Update the predictor (give it a sample) if it learns
            # # predictor.update(red,blue,nw,ne,sw)

            # Update currently known to the real value
            etknown[2*y+2,2*x+2] = nw-err_nw
            etknown[2*y+2,2*x+3] = ne-err_ne
            etknown[2*y+3,2*x+2] = sw-err_sw

    return errors

def retrieve_errors(prev,mat):

    # Save pixels from odd dimensions explicitly and trim borders
    borders = []
    if mat.shape[0]%2==1:
        borders.append(mat[-1,:])
    if mat.shape[1]%2==1:
        borders.append(mat[:,-1])
    mat = mat[:mat.shape[0]-mat.shape[0]%2,:mat.shape[1]-mat.shape[1]%2]

    if mat.size>0:
        # Extended prev matrix
        errors = get_errors(prev,mat);
    else:
        errors = np.zeros(1,dtype=np.int32)[:0]

    # Return errors and borders
    return errors,borders

def compress_mat(mat):

    # Numbers to save
    errors = [] # List of arrays of errors to be stored.
    borders = [] # List of borders to be stored.

    # Get all miniatures
    minis = get_miniatures(mat)
    for i in range(len(minis)):
        err,bors = retrieve_errors(None if i==0 else minis[i-1],minis[i])
        if len(err)>0:
            errors.append(err)
        for bor in bors:
            borders.append(bor)

    # Concatenate errors and borders
    errors = np.concatenate(errors,axis=None)
    borders = np.concatenate(borders,axis=None)

    return errors,borders
