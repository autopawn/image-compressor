from numba import jit
import numpy as np

from .predictors import predict

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

            # Update errors
            errors[i+0] = err_nw;
            errors[i+1] = err_ne;
            errors[i+2] = err_sw;
            i += 3

            # Update the predictor here (give it a sample) if it learns
            # # predictor.update(red,blue,mat[2*y,2*x],mat[2*y,2*x+1],mat[2*y+1,2*x])

            # Update currently known to the real value
            etknown[2*y+2,2*x+2] = nw-err_nw
            etknown[2*y+2,2*x+3] = ne-err_ne
            etknown[2*y+3,2*x+2] = sw-err_sw

    return errors

@jit('void(int32[:,:],int32[:,:],int32[:])',nopython=True)
def reconstruct_mat_from_errors(prev,mat,errors):
    # Extended prev matrix
    etprev = extend(prev)

    # Image currently known
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
            # Update matrix
            mat[2*y,2*x] = nw-errors[i+0]
            mat[2*y,2*x+1] = ne-errors[i+1]
            mat[2*y+1,2*x] = sw-errors[i+2]
            i += 3
            # copy already known byte
            mat[2*y+1,2*x+1] = etknown[2*y+3,2*x+3]

            # Update the predictor here (give it a sample) if it learns
            # # predictor.update(red,blue,mat[2*y,2*x],mat[2*y,2*x+1],mat[2*y+1,2*x])

            # Update currently known to the real value
            etknown[2*y+2,2*x+2] = mat[2*y,2*x]
            etknown[2*y+2,2*x+3] = mat[2*y,2*x+1]
            etknown[2*y+3,2*x+2] = mat[2*y+1,2*x]


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

def decompress_mat(shape,errors,borders):
    mshapes = get_miniature_shapes(shape)

    # Last completed miniature
    prev = None

    for shap in mshapes:
        mat = np.zeros(shap,np.int32)

        # Put borders:
        if mat.shape[0]%2==1:
            mat[-1,:] = borders[:shap[1]]
            borders = borders[shap[1]:]
        if mat.shape[1]%2==1:
            mat[:,-1] = borders[:shap[0]]
            borders = borders[shap[0]:]

        # Reconstruct mat from errors
        if prev is not None:
            n_errs = (mat.shape[0]-mat.shape[0]%2)*(mat.shape[1]-mat.shape[1]%2)*3//4
            reconstruct_mat_from_errors(prev,mat,errors)
            errors = errors[n_errs:]

        prev = mat

    return mat
