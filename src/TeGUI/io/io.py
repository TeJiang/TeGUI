
from src.TeGUI.cube_analysis.cube import Cube
from src.TeGUI.image_analysis.image import RGBImage, GrayscaleImage
from src.TeGUI.spectrum_analysis.spectrum import SinglePixelSpectrum, MultiSpectra
from src.TeGUI.roi_analysis.roi import ROI
from src.TeGUI.data_analysis.example_data import ExampleData
class IO:
    @staticmethod
    def load_cube(file_path):
        data = IO._read_file(file_path)
        return Cube(data)

    @staticmethod
    def load_image(file_path, image_type='rgb'):
        data = IO._read_file(file_path)
        if image_type == 'rgb':
            return RGBImage(data)
        elif image_type == 'grayscale':
            return GrayscaleImage(data)
        else:
            raise ValueError("Unknown image type")

    @staticmethod
    def load_spectrum(file_path, spectrum_type='single'):
        data = IO._read_file(file_path)
        if spectrum_type == 'single':
            return SinglePixelSpectrum(data)
        elif spectrum_type == 'multiple':
            return MultiSpectra(data)
        else:
            raise ValueError("Unknown spectrum type")

    @staticmethod
    def load_roi(file_path):
        points = IO._read_file(file_path)
        return ROI(points)

    @staticmethod
    def _read_file(file_path):
        # Logic to read the file and return data
        with open(file_path, 'r') as file:
            data = file.read()
        return data

    @staticmethod
    def save_data(file_path, data):
        # Logic to save data to a file
        with open(file_path, 'w') as file:
            file.write(data)
