class ROI:
    def __init__(self, mz_values):
        self.mz_values = mz_values
        self.intensity_values = []
        self.rt_values = []
        self.extended = False