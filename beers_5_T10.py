import pymzml
import matplotlib as plt
import itertools
import numpy as np

mzml_file_5 = "data/Beer_multibeers_5_T10_POS.mzML"
run = pymzml.run.Reader(mzml_file_5, {2: 2e-05})

#for spec in itertools.islice(run, 1000):

rois = []
potential_rois = []
for spec in run:
    print("Now checking:", spec.ID)
    if len(rois) == 0:
        for mass in spec.mz:
            rois.append([mass])
    else:
        waiting_rois = []
        for mass in spec.mz:
            for roi in rois:
                initial_len = len(roi)
                difference = np.abs(mass - np.mean(roi))
                if difference <= 2:
                    roi.append(mass)
                else:
                    if [mass] not in waiting_rois:
                        waiting_rois.append([mass])
                if len(roi) == initial_len:
                    if len(roi) < 15:
                        rois.remove(roi)
                    elif len(roi) >= 15:
                        potential_rois.append(roi)
                        print("Potential roi found:", roi)
                        rois.remove(roi)

        rois.extend(list(waiting_rois))

print(potential_rois)