from src.TeGUI.image_analysis.image import RGBImage, GrayscaleImage
from src.TeGUI.spectrum_analysis.spectrum import SinglePixelSpectrum, MultiSpectra
# src/TeGUI/cube_analysis/cube.py

class Cube:
    def __init__(self, data):
        self.data = data

    def get_rgb_image(self, red_layer, green_layer, blue_layer):
        red = self.data[red_layer]
        green = self.data[green_layer]
        blue = self.data[blue_layer]
        return RGBImage(red, green, blue)

    def get_grey_image(self, layer):
        grey = self.data[layer]
        return GrayscaleImage(grey)

    def get_spectrum(self, pixel_coords):
        spectra = self.data[:, pixel_coords[0], pixel_coords[1]]
        return SinglePixelSpectrum(spectra)

    def get_multiple_spectra(self, pixel_coords_list):
        spectra_list = [self.data[:, coords[0], coords[1]] for coords in pixel_coords_list]
        return MultiSpectra(spectra_list)
