from numba import jit

import numpy as np
import scipy.interpolate

# Lagrange 2D interpolation based on: https://people.sc.fsu.edu/~jburkardt/cpp_src/lagrange_interp_2d/lagrange_interp_2d.cpp

@jit("float64(float64[:],int32,float64)")
def lagrange_basis_function_1d(xd,i,xi):
    yi = 1.0;
    if xi!=xd[i]:
        for j in range(xd.size):
            if j!=i:
                yi = yi * ( xi - xd[j] ) / ( xd[i] - xd[j] );
    return yi;

@jit("float64[:](float64[:],float64[:],float64[:],float64[:],float64[:])")
def lagrange_interp_2d(xd_1d,yd_1d,zd,xi,yi):
    ni = xi.size
    if zd.size!=xd_1d.size*yd_1d.size:
        print("Warning: zd has an incorrect number of values.")

    zi = np.zeros(ni)
    for k in range(ni):
        l = 0
        zi[k] = 0.0
        for j in range(yd_1d.size):
            for i in range(xd_1d.size):
                lx = lagrange_basis_function_1d(xd_1d,i,xi[k]);
                ly = lagrange_basis_function_1d(yd_1d,j,yi[k]);
                zi[k] = zi[k] + zd[l] * lx * ly;
                l = l + 1;
    return zi


@jit('float64[:](int32[:,:])',nopython=True)
def paeth3(b3x3):
    A = b3x3[0,0]
    B = b3x3[0,1]
    C = b3x3[0,2]
    D = b3x3[1,0]
    E = b3x3[2,0]
    F = b3x3[2,2]
    v = 0.25*(A+F-C-E)
    x = F+B+D-E-C-3.0*v
    y = F+D-E-2.0*v
    z = F+B-C-2.0*v
    r = np.zeros(3,dtype=np.float64)
    r[0] = x
    r[1] = y
    r[2] = z
    return r

# @jit('float64[:](int32[:,:])',nopython=True)
# def large_paeth(b):
#     r = np.zeros(3,dtype=np.float64)
#     nw = b[2,1]+b[1,2]-b[1,1]
#     ne = b[1,3]+nw-b[1,2]
#     sw = b[3,1]+nw-b[2,1]
#     r[0] = nw
#     r[1] = ne
#     r[2] = sw
#     return r

# def super_paeth(b):
#     n = b.shape[0]
#     if n==2:
#         b[1,1] = b[0,1]+b[1,0]-b[0,0]
#         return b
#     else:
#         dy = super_paeth(b[1:,:-1]-b[:-1,:-1])
#         dx = super_paeth(b[:-1,1:]-b[:-1,:-1])
#         for b in


@jit('Tuple((int32,int32,int32))(int32[:,:],int32[:,:])',nopython=True)
def predict(red_px,blu_px):
    # Points to interpolate
    xis = np.array([2,3,2],dtype=np.float64)
    yis = np.array([2,2,3],dtype=np.float64)

    # Interpolate with red grid
    rgx = np.array([1,3,5],dtype=np.float64)
    rgy = np.array([1,3,5],dtype=np.float64)
    rgz = red_px.flatten().astype(np.float64)
    rzi = lagrange_interp_2d(rgx,rgy,rgz,xis,yis)
    rzi = np.minimum(np.maximum(rzi,0),255)

    # # Interpolate with blue grid 1
    # b1gx = np.array([0,1],dtype=np.float64)
    # b1gy = np.array([2,3],dtype=np.float64)
    # b1gz = blu_px[2:,:2].flatten().astype(np.float64)
    # b1zi = lagrange_interp_2d(b1gx,b1gy,b1gz,xis,yis)
    # b1zi = np.minimum(np.maximum(b1zi,0),255)
    #
    # # Interpolate with blue grid 2
    # b2gx = np.array([2,3],dtype=np.float64)
    # b2gy = np.array([0,1],dtype=np.float64)
    # b2gz = blu_px[:2,2:].flatten().astype(np.float64)
    # b2zi = lagrange_interp_2d(b2gx,b2gy,b2gz,xis,yis)
    # b2zi = np.minimum(np.maximum(b2zi,0),255)
    #
    # # Final predictions
    # fp = 0.66*rzi+0.17*b1zi+0.17*b2zi

    # pae = large_paeth(blu_px)
    pae = paeth3(blu_px[1:,1:])

    fp = 0.66*rzi+0.34*pae

    #
    nw = min(max(int(np.round(fp[0])),0),255)
    ne = min(max(int(np.round(fp[1])),0),255)
    sw = min(max(int(np.round(fp[2])),0),255)
    return nw,ne,sw


    # by = [0,0,0,0,1,1,1,1,2,2,3,3]
    # bx = [0,1,2,3,0,1,2,3,0,1,0,1]
    #
    # ry = [1,3,3,5,5,5]
    # rx = [5,3,5,1,3,5]
    #
    # py = np.array(by+ry)
    # px = np.array(bx+rx)
    #
    # bz = [
    #     blu_px[0,0],blu_px[0,1],blu_px[0,2],blu_px[0,3],
    #     blu_px[1,0],blu_px[1,1],blu_px[1,2],blu_px[1,3],
    #     blu_px[2,0],blu_px[2,1],
    #     blu_px[3,0],blu_px[3,1]                         ]
    # rz = [
    #                             red_px[0,2],
    #                 red_px[1,1],red_px[1,2],
    #     red_px[2,0],red_px[2,1],red_px[2,2]]
    #
    # pz = np.array(bz+rz)
