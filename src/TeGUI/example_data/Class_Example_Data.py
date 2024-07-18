import numpy as np
import random

class example_data():
    def __init__(self, x_num=256, y_num=256, wl_num=224):
        self.x_num, self.y_num, self.wl_num = x_num, y_num, wl_num
        self.wl_min, self.wl_max = 0.9, 3.65
        self.make_1d_wl()
        self.make_3d_cube()

    def make_1d_wl(self):
        self.wl = np.linspace(self.wl_min, self.wl_max, self.wl_num)
        self.rgb_indices = random.sample(range(self.wl_num), 3)
        self.rgb_channels = [self.wl[x] for x in self.rgb_indices]

    def make_3d_cube(self):
        self.cube = np.random.rand(self.x_num,self.y_num,self.wl_num)
        self.make_RGB_image()
        self.make_index_image()

    def make_RGB_image(self):
        self.RGB_image = self.cube[:, :, self.rgb_indices]
    def make_index_image(self):
        self.Index_image = np.nanmean(self.cube, axis=2)

if __name__ == '__main__':
    data = example_data()

