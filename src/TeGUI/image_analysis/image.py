import numpy as np
class Image:
    def __init__(self, data):
        self.image = data

    def display(self):
        # Generic display method, can be overridden by subclasses
        pass

class RGBImage(Image):
    def __init__(self, data):
        super().__init__(data)
        # Additional attributes specific to RGB images

    def rotate_cw(self):
        self.image = np.rot90(self.image, k=-1, axes=(0, 1))
    def rotate_acw(self):
        self.image = np.rot90(self.image, k=1, axes=(0, 1))
    def flip_ud(self):
        self.image = np.flip(self.image, axis=0)
    def flip_lr(self):
        self.image = np.flip(self.image, axis=1)
    def display(self):
        # Implementation for displaying RGB images
        print("Displaying RGB image")

    def to_grayscale(self):
        # Convert RGB image to grayscale
        pass

class GrayscaleImage(Image):
    def __init__(self, data):
        super().__init__(data)
        # Additional attributes specific to grayscale images

    def rotate_cw(self):
        self.image = np.rot90(self.image, k=-1)
    def rotate_acw(self):
        self.image = np.rot90(self.image, k=1)
    def flip_ud(self):
        self.image = np.flipud(self.image)
    def flip_lr(self):
        self.image = np.fliplr(self.image)
    def display(self):
        # Implementation for displaying grayscale images
        print("Displaying grayscale image")

# Example usage
if __name__ == "__main__":
    rgb_data = ...  # Load RGB image data
    grayscale_data = ...  # Load grayscale image data

    rgb_image = RGBImage(rgb_data)
    grayscale_image = GrayscaleImage(grayscale_data)

    rgb_image.display()
    grayscale_image.display()
