import numpy as np
class Wl_Wn():
    def __init__(self, x, x_type):
        self.x = x
        self.x_type = x_type

    def set_wl_wn(self):
        ### all the wl set to um unit
        if self.x_type == 'wl_nm':
            self.wl = self.x.copy()/1000
            self.wn = self.convert_wl_wn(self.wl)
        if self.x_type == 'wl_um':
            self.wl = self.x.copy()
            self.wn = self.convert_wl_wn(self.wl)
        if self.x_type == 'wn_cm':
            self.wn = self.x.copy()
            self.wl = self.convert_wl_wn(self.wn)

    def convert_wl_wn(self, x):
        return 10000/x

    def find_closest_value(self, ref_value, x_type_wl_or_wn="wl"):
        """
        Find the closest value and its index in the array to the reference value.

        Parameters:
        array (numpy.ndarray): The array of wavelength or wavenumber values.
        ref_value (float): The reference value to find the closest value to.

        Returns:
        tuple: A tuple containing the closest value and its index.

        Raises:
        ValueError: If the reference value is outside the range of the array.
        """
        if x_type_wl_or_wn == 'wl':
            array = self.wl.copy()
        elif x_type_wl_or_wn == 'wn':
            array = self.wn.copy()
        else:
            print(f"Invalid value for x_type, chose wl or wn")

        # Check if the reference value is outside the range of the array
        if ref_value < array.min() or ref_value > array.max():
            raise ValueError(
                f"Reference value {ref_value} is outside the range of the array ({array.min()}, {array.max()})")

        # Find the index of the closest value
        index = (np.abs(array - ref_value)).argmin()
        closest_value = array[index]

        return closest_value, index
    def find_duplicate(self):
        ...