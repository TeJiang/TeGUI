class Image:
    def __init__(self, data):
        self.data = data

    def display(self):
        # Generic display method, can be overridden by subclasses
        pass

class RGBImage(Image):
    def __init__(self, data):
        super().__init__(data)
        # Additional attributes specific to RGB images

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
