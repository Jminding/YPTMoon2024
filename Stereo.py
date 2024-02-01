import numpy as np
import cv2

def Stereo(directory, imagename, numImages):
    # Read the lights and directions:
    lightfile = directory + '/' + 'lights2.txt'
    fid = open(lightfile, 'r')
    numLights = 1
    numLights = int(fid.readline())
    LightMatrix = []
    for i in range(numLights):
        lightDir = np.array(fid.readline().split(), dtype=float)
        lightDir = lightDir / np.linalg.norm(lightDir)
        LightMatrix.append(lightDir)
    fid.close()
    
    # Read the mask file and threshold the values
    maskfile = directory + '/' + imagename + '/' + imagename + '.mask.tiff'
    maskImage = cv2.imread(maskfile, cv2.IMREAD_GRAYSCALE)
    nrows, ncols = maskImage.shape
    maxval = np.max(maskImage)
    for i in range(nrows):
        for j in range(ncols):
            if maskImage[i, j] == maxval:
                maskImage[i, j] = 1
            else:
                maskImage[i, j] = 0
    
    # Read all the images
    accumImage = np.zeros((nrows, ncols, 3))
    images = np.zeros((nrows, ncols, 3, numImages), dtype=np.uint8)
    grayImageSet = np.zeros((nrows, ncols, numImages), dtype=np.uint8)
    for im in range(numImages):
        id = str(im)
        filename = directory + '/' + imagename + '/' + imagename + '.' + id + '.tiff'
        newImage = cv2.imread(filename)
        if newImage.shape[0] != nrows or newImage.shape[1] != ncols:
            print('mask image and source image size do not match')
            return
        accumImage += newImage.astype(float)
        images[:, :, :, im] = newImage
        grayImageSet[:, :, im] = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    
    for i in range(nrows):
        for j in range(ncols):
            r = accumImage[i, j, 0]
            g = accumImage[i, j, 1]
            b = accumImage[i, j, 2]
            if r < 5.0 or g < 5.0 or b < 5.0:
                maskImage[i, j] = 0
    
    z = np.zeros((nrows, ncols))
    
    # Process Red Channel for Red Albedo
    surfNormals, albedo = NormalMap(images, LightMatrix, maskImage, 1)
    save_data(surfNormals, albedo, maskImage, z, 'redChannel.dat')
    
    # Process Green Channel for Green Albedo
    surfNormals, albedo = NormalMap(images, LightMatrix, maskImage, 2)
    save_data(surfNormals, albedo, maskImage, z, 'greenChannel.dat')
    
    # Process Blue Channel for Blue Albedo
    surfNormals, albedo = NormalMap(images, LightMatrix, maskImage, 3)
    save_data(surfNormals, albedo, maskImage, z, 'blueChannel.dat')
    
    # Use Gray channel for Normal and Depth Map
    surfNormals, albedo = NormalMap(images, LightMatrix, maskImage, 0)
    z = DepthMap(surfNormals, maskImage)
    save_data(surfNormals, albedo, maskImage, z, 'grayChannel.dat')
    
    # Display the depth map
    # surfl(z)
    # shading interp
    # colormap gray

def save_data(surfNormals, albedo, maskImage, z, filename):
    fid = open(filename, 'w')
    nrows, ncols = maskImage.shape
    xg = np.zeros((nrows, ncols))
    yg = np.zeros((nrows, ncols))
    for i in range(nrows):
        for j in range(ncols):
            xg[i, j] = float(j) / float(ncols)
            yg[i, j] = float(nrows - i + 1) / float(nrows)
    
    fid.write('{} {}\n'.format(nrows, ncols))
    for i in range(nrows):
        for j in range(ncols):
            nx = surfNormals[i, j, 0]
            ny = surfNormals[i, j, 1]
            nz = surfNormals[i, j, 2]
            alb = albedo[i, j]
            if maskImage[i, j]:
                msk = 1
            else:
                msk = 0
            fid.write('{} {} {} {} {} {} {} {}\n'.format(msk, xg[i, j], yg[i, j], z[i, j], nx, ny, nz, alb))
    fid.close()

def getPixelIndex(i, j, nrows, ncols):
    return (i - 1) * ncols + j


