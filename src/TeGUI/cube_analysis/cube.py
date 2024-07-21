'''
cube class is for storing the hyperspectral images
I choose to use [xx, yy, wl] format
1.	Ease of Understanding: [xx, yy, wl]: This format is often more intuitive because it mirrors
how we typically think of 	images (spatial dimensions first) and then consider the spectral
information at each pixel.
2.	Performance: Contiguity in Memory: NumPy arrays are stored in contiguous blocks of memory.
Access patterns that align with this contiguity are faster. By default, NumPy uses row-major
order (C-style), meaning that the last dimension varies the fastest. Thus, [xx, yy, wl] can
offer better performance for operations that involve accessing or iterating over pixels.
Indexing Efficiency: Operations that involve extracting spectra (i.e., all wavelengths at a
particular pixel) are efficient with the [xx, yy, wl] format. This is because you can access
the spectral dimension directly after specifying the spatial coordinates.
'''
import numpy as np
from src.TeGUI.image_analysis.image import RGBImage, GrayscaleImage
from src.TeGUI.spectrum_analysis.spectrum import SinglePixelSpectrum, MultiSpectra

class Cube:
    def __init__(self, data):
        # default as [xx, yy, wl], numpy array
        self.cube = data
        self.cube_original = self.cube.copy()
        self.r_image, self.g_image, self.b_image, self.rgb_image = None, None, None, None
    def rotate_cw(self):
        self.cube = np.rot90(self.cube, k=-1, axes=(0, 1))
    def rotate_acw(self):
        self.cube = np.rot90(self.cube, k=-1, axes=(1, 0))
    def flip_lr(self):
        self.cube = np.flip(self.cube, axis=1)
    def flip_ud(self):
        self.cube = np.flip(self.cube, axis=0)
    def set_rgb_image_from_index(self, r_pos, g_pos, b_pos):
        self.r_image = self.cube[:, :, r_pos]
        self.g_image = self.cube[:, :, g_pos]
        self.b_image = self.cube[:, :, b_pos]

        self.rgb_image = RGBImage(self.cube[:, :, [r_pos, g_pos, b_pos]])
    def set_grey_image_from_index(self, pos):
        self.grey_image = GrayscaleImage(self.cube[:, :, pos])
