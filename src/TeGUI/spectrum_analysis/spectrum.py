class Spectrum:
    def __init__(self, data):
        self.data = data

    def analyze(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    def plot(self):
        # Common plotting logic, if applicable
        pass



class SinglePixelSpectrum(Spectrum):
    def __init__(self, data):
        super().__init__(data)

    def analyze(self):
        # Analysis logic specific to single pixel spectrum
        print("Analyzing single pixel spectrum")

    def plot(self):
        # Plotting logic specific to single pixel spectrum
        print("Plotting single pixel spectrum")

class MultiSpectra(Spectrum):
    def __init__(self, data):
        super().__init__(data)

    def analyze(self):
        # Analysis logic specific to multiple spectra
        print("Analyzing multiple spectra")

    def plot(self):
        # Plotting logic specific to multiple spectra
        print("Plotting multiple spectra")
