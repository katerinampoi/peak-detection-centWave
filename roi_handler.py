import numpy as np


class ROI:
    def __init__(self, mz_values):
        self.mz_values = mz_values
        self.mz_mean = np.mean(mz_values)
        self.extended = False
        self.intensity_values = []
        self.retention_time_values = []

    def __lt__(self, other):
        return self.mz_mean < other

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

    def get_intensity_values(self):
        return self.intensity_values

    def get_retention_time_values(self):
        return self.retention_time_values







