from numba import jit

import numpy as np
import scipy.interpolate

class Predictor():
    def __init__(self):
        self.reset()
    def reset(self):
        pass
    def predict(self,red_px,blu_px):
        # Should not modify self!!
        pass
    def update(self,red_px,blu_px,nw,ne,sw):
        pass

class RegularInterpolator(Predictor):

    @jit(forceobj=True)
    def predict(self,red_px,blu_px):
        by = [0,0,0,0,1,1,1,1,2,2,3,3]
        bx = [0,1,2,3,0,1,2,3,0,1,0,1]

        ry = [1,3,3,5,5,5]
        rx = [5,3,5,1,3,5]

        py = np.array(by+ry)
        px = np.array(bx+rx)

        bz = [
            blu_px[0,0],blu_px[0,1],blu_px[0,2],blu_px[0,3],
            blu_px[1,0],blu_px[1,1],blu_px[1,2],blu_px[1,3],
            blu_px[2,0],blu_px[2,1],
            blu_px[3,0],blu_px[3,1]                         ]
        rz = [
                                    red_px[0,2],
                        red_px[1,1],red_px[1,2],
            red_px[2,0],red_px[2,1],red_px[2,2]]

        pz = np.array(bz+rz)

        f = scipy.interpolate.Rbf(*(px,py,pz))
        nw = min(max(0,int(round(float(f(2,2))))),255)
        ne = min(max(0,int(round(float(f(3,2))))),255)
        sw = min(max(0,int(round(float(f(2,3))))),255)

        return nw,ne,sw
