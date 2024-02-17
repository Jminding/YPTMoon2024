# 2024 Young Physicists Tournament Moon Project

This was the project presented by Rye Country Day School for the 2024 US Invitational Young Physicists Tournament. Rye Country Day School is the 2024 USIYPT Champion.
<hr>


Since the files are super messy, here's a small breakdown of important files to this project:

### Files
- 📄 `angle.py`: Contains functions for calculating angles between the sun, earth, and moon using right ascension and declination
- 📄 `coordinates.py`: A custom file for custom coordinate classes (rectangular and spherical)
- 📄 `create_light_directions.py`: Calculates the light source direction vectors and saves them for use in photometric stereo
- 📄 `photometric_stereo_3.ipynb`: Performs the photometric stereo algorithm on images of the full moon
- 📄 `photometric_stereo_5.ipynb`: Performs the photometric stereo algorithm on images of Copernicus Crater
- 📄 `render_copernicus.py`: Renders a 3D heightmap for Copernicus Crater
- 📄 `render_copernicus_cropped.py`: Renders a 3D heightmap for a cropped version of Copernicus Crater to compare it with a rendered heightmap of it downloaded from NASA's website
- 📄 `render_moon.py`: Renders a 3D heightmap for the entire moon
- 📄 `copernicus_comparison.py`: Compares our rendered model with NASA's 3D model

### Directories
- 📁 `test_data_libration/`: Contains images of the full moon that account for libration
- 📁 `Copernicus Cropped/`: Contains images of the Copernicus Crater that account for libration (not included in this repo)

## Explanation
There's three parts to this project:
1. Data Collection<br>
We started out taking images of the moon, but decided to use images from NASA SVS Dial-A-Moon instead.<br>
In order to remove libration, we manually edited a lot of images so that features matched up, and used a little MATLAB in the process. 

2. Photometric Stereo<br>
We then decided to create a normal map of the moon using the photometric stereo algorithm, first proposed by Robert J. Woodham from the University of British Columbia in 1980.<br>
The key formula here is $I = \dfrac{\rho}{\pi} \hat{s}\cdot \hat{n}$, where $I$ is the intensity of a given pixel, $\rho$ is the albedo (reflectance) at that point, $\hat{s}$ is the light source direction vector at that point, and $\hat{n}$ is unit surface normal vector at that pixel.

3. Heightmap Rendering<br>
In order to turn the surface normals into a 3D model, we decided to add up the components of the normal vectors like a Riemann Sum.<br>
In particular, for the $x$-direction, the change in height is $h_x = \dfrac{n_x}{n_z}d$, where $d$ is the length of 1 pixel. The same can be applied to the $y$-direction.

## Rendered 3D models:
1. Copernicus Crater (full): [https://jminding.github.io/YPTMoon2023/output/copernicus_heightmap.html](https://jminding.github.io/YPTMoon2023/output/copernicus_heightmap.html)
2. Copernicus Crater (cropped): [https://jminding.github.io/YPTMoon2023/output/copernicus_heightmap_cropped.html](https://jminding.github.io/YPTMoon2023/output/copernicus_heightmap_cropped.html)
3. Full Moon: [https://jminding.github.io/YPTMoon2023/output/fullmoon_heightmap.html](https://jminding.github.io/YPTMoon2023/output/fullmoon_heightmap.html)