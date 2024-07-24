"""
the Data class include all the data of one sample, indluding cubes, images, spectrum, etc
although one sample can have several cubes, images, but normally, the number is one
"""
from src.TeGUI.cube_analysis.cube import Cube
from src.TeGUI.image_analysis.image import RGBImage, GrayscaleImage
from src.TeGUI.spectrum_analysis.spectrum import Spectrum
from src.TeGUI.data_analysis.sample import Sample
class Data():
    def __init__(self):
        self.visible_image = None
        self.visible_image_list = []

        self.cube = None
        self.cube_list = []

    def set_visible_image(self, visible_image):
        self.visible_image = RGBImage(visible_image)
    def set_visible_image_list(self, visible_image_list):
        self.visible_image_list = visible_image_list

    def set_cube(self, cube, x, x_type):
        self.cube = Cube(cube, x, x_type)
    def set_cube_list(self, cube_list, x_list, x_type_list):
        for (cube, x, x_type) in zip(cube_list, x_list, x_type_list):
            self.cube_list.append(Cube(cube, x, x_type))