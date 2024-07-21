"""
the Data class include all the data of one sample, indluding cubes, images, spectrum, etc
although one sample can have several cubes, images, but normally, the number is one
"""
from src.TeGUI.cube_analysis.cube import Cube
from src.TeGUI.image_analysis.image import Image
from src.TeGUI.spectrum_analysis.spectrum import Spectrum
from src.TeGUI.data_analysis.sample import Sample
class Data():
    def __init__(self):
        self.visible_image = None
        self.visible_image_list = []

        self.cube = None
        self.cube_list = []

        self.wl = None
        self.wl_list = []
