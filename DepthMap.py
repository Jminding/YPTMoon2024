import numpy as np
from scipy.sparse import lil_matrix

def DepthMap(surfNormals, maskImage):
    z = []
    nrows = maskImage.shape[0]
    ncols = maskImage.shape[1]
    objectPixelRow, objectPixelCol = np.where(maskImage)
    objectPixels = np.column_stack((objectPixelRow, objectPixelCol))
    
    index = np.zeros((nrows, ncols))
    numPixels = objectPixels.shape[0]
    
    for d in range(numPixels):
        pRow = objectPixels[d, 0]
        pCol = objectPixels[d, 1]
        index[pRow, pCol] = d+1
    
    M = lil_matrix((2*numPixels, numPixels))
    b = np.zeros((2*numPixels, 1))
    
    for d in range(numPixels):
        pRow = objectPixels[d, 0]
        pCol = objectPixels[d, 1]
        nx = surfNormals[pRow, pCol, 0]
        ny = surfNormals[pRow, pCol, 1]
        nz = surfNormals[pRow, pCol, 2]
        
        if (index[pRow, pCol+1] > 0) and (index[pRow-1, pCol] > 0):
            M[2*d, index[pRow, pCol]-1] = 1
            M[2*d, index[pRow, pCol+1]-1] = -1
            b[2*d, 0] = nx / nz
            M[2*d+1, index[pRow, pCol]-1] = 1
            M[2*d+1, index[pRow-1, pCol]-1] = -1
            b[2*d+1, 0] = ny / nz
        elif (index[pRow-1, pCol] > 0):
            f = -1
            if (index[pRow, pCol+f] > 0):
                M[2*d, index[pRow, pCol]-1] = 1
                M[2*d, index[pRow, pCol+f]-1] = -1
                b[2*d, 0] = f * nx / nz
            M[2*d+1, index[pRow, pCol]-1] = 1
            M[2*d+1, index[pRow-1, pCol]-1] = -1
            b[2*d+1, 0] = ny / nz
        elif (index[pRow, pCol+1] > 0):
            f = -1
            if (index[pRow-f, pCol] > 0):
                M[2*d+1, index[pRow, pCol]-1] = 1
                M[2*d+1, index[pRow-f, pCol]-1] = -1
                b[2*d+1, 0] = f * ny / nz
            M[2*d, index[pRow, pCol]-1] = 1
            M[2*d, index[pRow, pCol+1]-1] = -1
            b[2*d, 0] = nx / nz
        else:
            f = -1
            if (index[pRow, pCol+f] > 0):
                M[2*d, index[pRow, pCol]-1] = 1
                M[2*d, index[pRow, pCol+f]-1] = -1
                b[2*d, 0] = f * nx / nz
            f = -1
            if (index[pRow-f, pCol] > 0):
                M[2*d+1, index[pRow, pCol]-1] = 1
                M[2*d+1, index[pRow-f, pCol]-1] = -1
                b[2*d+1, 0] = f * ny / nz
    
    x = np.linalg.lstsq(M.tocsr(), b, rcond=None)[0]
    x = x - np.min(x)
    
    tempShape = np.zeros((nrows, ncols))
    
    for d in range(numPixels):
        pRow = objectPixels[d, 0]
        pCol = objectPixels[d, 1]
        tempShape[pRow, pCol] = x[d, 0]
    
    z = np.zeros((nrows, ncols))
    
    for i in range(nrows):
        for j in range(ncols):
            z[i, j] = tempShape[nrows-i-1, j]
    
    return z

def getPixelIndex(i, j, nrows, ncols):
    id = (i-1)*ncols + j
    return id


