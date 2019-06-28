import numpy as np

# Creates a larger matrix by extending the borders
def extend(mat):
    etmat = np.zeros((mat.shape[0]+2,mat.shape[1]+2))
    etmat[1:-1,1:-1] = mat
    etmat[:,0] = etmat[:,1]
    etmat[:,-1] = etmat[:,-2]
    etmat[0,:] = etmat[1,:]
    etmat[-1,:] = etmat[-2,:]
    return etmat

# Rescales a matrix by the double of its size
def scale2x(mat):
    dmat = np.zeros((mat.shape[0]*2,mat.shape[1]*2))
    dmat[0::2,0::2] = mat
    dmat[0::2,1::2] = mat
    dmat[1::2,0::2] = mat
    dmat[1::2,1::2] = mat
    return dmat


# Gets the shapes that each miniature should have
def get_miniature_shapes(shape):
    shape = tuple(shape)
    shapes = [shape]
    while 1:
        shape = (shape[0]//2,shape[1]//2)
        if shape[0]==0 or shape[1]==0: break
        shapes.append(shape)
    return shapes[::-1]

# Gets the miniatures of the original image, by
def get_miniatures(mat):
    mats = [mat]
    while mat.shape != (1,1):
        mat = mat[1::2,1::2]
        if mat.size==0: break
        mats.append(mat)
    return mats[::-1]
