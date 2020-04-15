import numpy as np


class ROI:
    def __init__(self, mz_values):
        self.mz_values = mz_values
        self.intensity_values = []
        self.RT_values = []
        self.extended = False
        self.mz_mean = np.mean(mz_values)

    def get_mz_values(self):
        return self.mz_values

    def add_mz_value(self, mz_value):
        self.mz_values.append(mz_value)

    def get_mz_mean(self):
        return self.mz_mean

    def update_mz_mean(self):
        self.mz_mean = np.mean(self.mz_values)

    def get_extended(self):
        return self.extended

    def set_extended(self, extended):
        self.extended = extended




