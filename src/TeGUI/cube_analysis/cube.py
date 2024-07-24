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
from src.TeGUI.spectrum_analysis.wl_wn import Wl_Wn

class Cube:
    def __init__(self, cube, x, x_type="wl_um"):
        # default as [xx, yy, wl], numpy array
        self.cube =cube
        self.x = x
        self.x_type = x_type # "wl_nm", "wl_um", "wn_cm"
        self.set_wl_wn()
        self.cube_original = self.cube.copy()
        self.r_image, self.g_image, self.b_image, self.rgb_image = None, None, None, None
        self.gray_image = None

        self.cal_brightness()
    def set_wl_wn(self):
        self.wl_wn = Wl_Wn(x=self.x, x_type=self.x_type)
    def rotate_cw(self):
        self.cube = np.rot90(self.cube, k=-1, axes=(0, 1))
    def rotate_acw(self):
        self.cube = np.rot90(self.cube, k=1, axes=(0, 1))
    def flip_lr(self):
        self.cube = np.flip(self.cube, axis=1)
    def flip_ud(self):
        self.cube = np.flip(self.cube, axis=0)
    def set_rgb_image_from_value(self, r_value, g_value, b_value):
        self.r_value_c, self.r_pos = self.wl_wn.find_closest_value(ref_value=r_value,x_type_wl_or_wn='wl')
        self.g_value_c, self.g_pos = self.wl_wn.find_closest_value(ref_value=g_value, x_type_wl_or_wn='wl')
        self.b_value_c, self.b_pos = self.wl_wn.find_closest_value(ref_value=b_value, x_type_wl_or_wn='wl')
        print(self.r_value_c, self.r_pos)
        self.set_rgb_image_from_index(self.r_pos, self.g_pos, self.b_pos)

    def set_rgb_image_from_index(self, r_pos, g_pos, b_pos):
        self.r_pos, self.g_pos, self.b_pos = r_pos, g_pos, b_pos
        # find corresponding rgb values, depends on wl, wn
        if self.x_type == "wl_um" or self.x_type == "wl_nm":
            self.r_value_c, self.g_value_c, self.b_value_c = self.wl_wn.wl[self.r_pos], self.wl_wn.wl[self.g_pos], self.wl_wn.wl[self.b_pos]
        elif self.x_type == "wn_cm":
            self.r_value_c, self.g_value_c, self.b_value_c = self.wl_wn.wn[self.r_pos], self.wl_wn.wn[self.g_pos], self.wl_wn.wn[self.b_pos]
        # creat r g b layers
        self.r_image = self.cube[:, :, self.r_pos]
        self.g_image = self.cube[:, :, self.g_pos]
        self.b_image = self.cube[:, :, self.b_pos]

        # creat rgb image
        self.rgb_image = RGBImage(self.cube[:, :, [self.r_pos, self.g_pos, self.b_pos]])
    def set_grey_image_from_index(self, pos):
        self.grey_pos = pos
        if self.x_type == "wl_um" or self.x_type == "wl_nm":
            self.grey_value = self.wl_wn.wl[self.grey_pos]
        elif self.x_type == "wn_cm":
            self.grey_value = self.wl_wn.wn[self.grey_pos]
        self.grey_image = GrayscaleImage(self.cube[:, :, pos])
    def cal_brightness(self):
        self.brightness = GrayscaleImage(np.average(self.cube, axis=2))