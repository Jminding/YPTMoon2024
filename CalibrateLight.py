import os
import cv2
import numpy as np

def CalibrateLight(directory, numLights):
    # This function is used to calibrate the lighting direction.
    # Find all the files in that directory.
    if directory[-1] != '/':
        fileName = directory + '/'
    else:
        fileName = directory
    fileName = fileName + 'chrome.'
    
    # Calculate the center of the chrome ball.
    maskFileName = fileName + 'mask.tiff'
    circle = cv2.imread(maskFileName, cv2.IMREAD_GRAYSCALE)
    
    # Calculate the center of the chrome ball.
    maxval = np.max(circle)
    circleRow, circleCol = np.where(circle == maxval)
    maxRow = np.max(circleRow)
    minRow = np.min(circleRow)
    maxCol = np.max(circleCol)
    minCol = np.min(circleCol)
    xc = float((maxCol + minCol) / 2)
    yc = float((maxRow + minRow) / 2)
    center = [xc, yc]
    radius = float((maxRow - minRow) / 2)
    
    # R: The reflection direction.
    R = [0, 0, 1.0]
    L = []
    
    # Calculate the lighting direction.
    for i in range(1, numLights + 1):
        imgFileName = fileName + str(i - 1) + '.tiff'
        image = cv2.imread(imgFileName, cv2.IMREAD_GRAYSCALE)
        maxval = np.max(image)
        pointRow, pointCol = np.where(image == maxval)
        nSize = pointRow.shape[0]
        px = np.sum(pointCol) / float(nSize)
        py = np.sum(pointRow) / float(nSize)
        Nx = px - xc
        Ny = -(py - yc)
        Nz = np.sqrt(radius**2 - Nx**2 - Ny**2)
        normal = [Nx, Ny, Nz]
        normal = normal / radius
        NR = normal[0] * R[0] + normal[1] * R[1] + normal[2] * R[2]
        L.append(2 * NR * normal - R)
    
    # Write the new lighting direction into a test file.
    with open('calibratedLight.txt', 'w') as fid:
        fid.write(str(numLights) + '\n')
        for row in L:
            fid.write(' %10.5f %10.5f %10.5f \n' % (row[0], row[1], row[2]))
    
    return L


