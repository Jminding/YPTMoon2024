import numpy as np

def NormalMap(images, lightMatrix, maskImage, whichChannel):
    surfNormals = np.zeros(images.shape[1:])
    albedo = np.zeros(images.shape[1:3])
    numImages, nrows, ncols, numColors = images.shape
    
    for i in range(nrows):
        for j in range(ncols):
            surfNormals[i,j,0] = 0.0
            surfNormals[i,j,1] = 0.0
            surfNormals[i,j,2] = 1.0
            albedo[i,j] = 0.0
    
    if whichChannel == 0:
        grayimages = np.zeros((numImages, nrows, ncols))
        for im in range(numImages):
            grayimages[im] = np.dot(images[im], [0.2989, 0.5870, 0.1140])
        
    #     for i in range(nrows):
    #         for j in range(ncols):
    #             if maskImage[i,j]:
    #                 I = np.zeros(numImages)
    #                 for im in range(numImages):
    #                     I[im] = float(grayimages[i,j,im])
    #                 NP, R, fail = PixelNormal(I, lightMatrix)
    #                 surfNormals[i,j,0] = NP[0]
    #                 surfNormals[i,j,1] = NP[1]
    #                 surfNormals[i,j,2] = NP[2]
    #                 albedo[i,j] = R
    
    if whichChannel > 0:
        for i in range(nrows):
            for j in range(ncols):
                if maskImage[i,j]:
                    I = np.zeros(numImages)
                    for im in range(numImages):
                        I[im] = float(images[i,j,whichChannel-1,im])
                    NP, R, fail = PixelNormal(I, lightMatrix)
                    surfNormals[i,j,0] = NP[0]
                    surfNormals[i,j,1] = NP[1]
                    surfNormals[i,j,2] = NP[2]
                    albedo[i,j] = R
    
    maxval = np.max(albedo)
    if maxval > 0:
        albedo = albedo / maxval
    
    return surfNormals, albedo

def PixelNormal(I, L):
    fail = 0
    I = I.T
    LT = L.T
    A = np.dot(LT, L)
    b = np.dot(LT, I)
    g = np.linalg.inv(A).dot(b)
    R = np.linalg.norm(g)
    N = g / R
    
    if np.linalg.norm(I) < 1.0E-06:
        print('Warning: Pixel intensity is zero')
        N[0] = 0.0
        N[1] = 0.0
        N[2] = 0.0
        R = 0.0
        fail = 1
    
    return N, R, fail