import pymzml
import matplotlib as plt
import itertools
import numpy as np

mzml_file = "data/Beer_multibeers_5_T10_POS.mzML"
run = pymzml.run.Reader(mzml_file)

rois = []
final_rois = []
max_difference = 20
p_min = 15

# Initialization - Add the first m/z in the rois list
for spec in run:
    print("Now checking:", spec.ID)
    if len(rois) == 0:
        for mass in spec.mz:
            rois.append([mass])
# For current scan, add m/z to roi in rois, depending on the mass value
    else:
        waiting_rois = []       # m/z from current scan that didn't meet the condition in line 27 are added in this list
        for mass in spec.mz:
            for roi in rois:
                initial_len = len(roi)
                difference = np.abs(mass - np.mean(roi))
                if difference <= max_difference:
                    roi.append(mass)
                else:
                    if [mass] not in waiting_rois:
                        waiting_rois.append([mass])

                if len(roi) == initial_len:     # Check if rois are extended to the next step, based on the roi's length
                    if len(roi) < p_min:        # Remove the rois not extended and containing less than p_min centroids
                        rois.remove(roi)
                    elif len(roi) >= p_min:     # Keep the rois not extended and containing at least p_min centroids
                        final_rois.append(roi)
                        print("ROI found")
                        rois.remove(roi)

        rois.extend(list(waiting_rois))         # Merge waiting list and rois list

print(final_rois)