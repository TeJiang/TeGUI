import numpy as np
import random
from scipy.ndimage import gaussian_filter

from src.TeGUI.data_analysis.data import Data


class ExampleData(Data):
    def __init__(self, x_num=256, y_num=256, wl_num=224):
        super().__init__()
        self.x_num, self.y_num, self.wl_num = x_num, y_num, wl_num
        self.wl_min, self.wl_max = 0.9, 3.65
        self.set_data()

    def gaussian(self, x, mu, sigma, intensity):
        return intensity * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))

    def generate_baseline(self, wl):
        # Create a smooth increasing continuum
        return 0.5 + 0.5 * (wl - wl.min()) / (wl.max() - wl.min())

    def generate_irregular_mask(self, size, intensity_variation):
        # Generate a random irregular mask
        mask = np.random.rand(size, size)
        mask = gaussian_filter(mask, sigma=3)
        mask = (mask > 0.5).astype(float)
        mask *= np.random.uniform(0.5, 1.0, size=(size, size)) * intensity_variation
        return gaussian_filter(mask, sigma=2)  # Increase sigma for more blurring

    def set_data(self):
        # Generate wavelength values
        wl = np.linspace(self.wl_min, self.wl_max, self.wl_num)

        # Initialize the hyperspectral cube with the baseline continuum
        baseline = self.generate_baseline(wl)
        cube = np.tile(baseline, (self.x_num, self.y_num, 1))

        # Add small random noise to the cube
        noise_level = 0.03
        cube += np.random.rand(self.x_num, self.y_num, self.wl_num) * noise_level

        # Define absorption features
        absorption_features = {
            "OH": (2.7, 0.05, 0.5),
            "NH": (3.06, 0.05, 0.1),
            "CH1": (3.4, 0.05, 0.3),
            "CH2": (3.5, 0.05, 0.3)
        }

        # Create clusters with varying absorption intensities and irregular shapes
        num_clusters = 5
        max_cluster_size = 30
        for _ in range(num_clusters):
            cx, cy = random.randint(0, self.x_num - max_cluster_size), random.randint(0, self.y_num - max_cluster_size)
            cluster_size = random.randint(15, max_cluster_size)
            intensity_variation = np.random.uniform(0.5, 1.0)
            mask = self.generate_irregular_mask(cluster_size, intensity_variation)
            for feature, (center, sigma, intensity) in absorption_features.items():
                for i in range(cluster_size):
                    for j in range(cluster_size):
                        x_idx = cx + i
                        y_idx = cy + j
                        if x_idx < self.x_num and y_idx < self.y_num:
                            cube[x_idx, y_idx, :] -= mask[i, j] * self.gaussian(wl, center, sigma, intensity)

        # Add heterogeneous background with OH absorption
        background_mask = self.generate_irregular_mask(self.x_num, 0.4)
        for i in range(self.x_num):
            for j in range(self.y_num):
                cube[i, j, :] -= self.gaussian(wl, 2.7, 0.05, 0.25 * background_mask[i, j])

        # Introduce dead and hot pixels
        num_dead_pixels = int(0.01 * self.x_num * self.y_num)  # 1% of the pixels
        num_hot_pixels = int(0.01 * self.x_num * self.y_num)  # 1% of the pixels

        for _ in range(num_dead_pixels):
            x, y = random.randint(0, self.x_num - 1), random.randint(0, self.y_num - 1)
            cube[x, y, :] = 0  # Dead pixel

        for _ in range(num_hot_pixels):
            x, y = random.randint(0, self.x_num - 1), random.randint(0, self.y_num - 1)
            cube[x, y, :] = 1  # Hot pixel

        # Scale the entire cube to have an average brightness of 3-4%
        desired_brightness = 0.035  # Average brightness of 3.5%
        current_mean = np.mean(cube)
        scaling_factor = desired_brightness / current_mean
        cube *= scaling_factor

        # Ensure the cube values are within a realistic range
        cube = np.clip(cube, 0, 1)

        self.set_cube(cube, wl, "wl_um")

        # Set RGB image from specific wavelength values
        r_value, g_value, b_value = 2.5, 2.7, 3.4
        self.cube.set_rgb_image_from_value(r_value, g_value, b_value)
        print(self.cube.r_value_c)


if __name__ == '__main__':
    data = ExampleData()