import pymzml
import matplotlib as plt
import itertools
import numpy as np
from roi_handler import ROI
import bisect

mzml_file = "data/Beer_multibeers_5_T10_POS.mzML"
# run = pymzml.run.Reader(mzml_file)


def find_rois(run):
    rois = []
    final_rois = []
    max_difference = 20
    p_min = 10

    # Initialization - ROI(mz_values) added to rois
    for spec in run:
        if len(rois) == 0:
            for mass in spec:
                roi = ROI(mz_values=[mass])
                rois.append(roi)

    # For current scan, add mass to ROI(mz_values) in rois
        else:
            for roi in rois:
                roi.extended = False    # for every new scan, roi is taken as not extended
            waiting_rois = []           # masses not been matched in this loop
            for mass in spec:
                print("Now checking mass:", mass)
                mass_added = False
                rois.sort(key=lambda x: x.mz_mean) # rois are sorted according to ROI(mz_values) mean
                for roi in rois:
                    print("Now checking roi:", roi.mz_values, roi.extended)
                    difference = np.abs(mass - roi.mz_mean)
                    if difference <= max_difference:
                        roi.mz_values.append(mass)
                        roi.mz_mean = np.mean(roi.mz_values)     # mean updated
                        roi.extended = True
                        print("mass added")
                        mass_added = True
                        break   # mass only goes into one roi

                if not mass_added:
                    waiting_rois.append(ROI(mz_values=[mass]))
                    print('Waiting rois now: ', [roi.mz_values for roi in waiting_rois])
            for roi in rois:
                print("clear phase: Roi:", roi.mz_values, roi.extended)
                if not roi.extended:
                    if len(roi.mz_values) < p_min:
                        print('Now removing roi:', roi.mz_values)
                        rois.remove(roi)
                    elif len(roi.mz_values) >= p_min:
                        print('Now adding roi:', roi.mz_values)
                        final_rois.append(roi)

            rois.extend(list(waiting_rois))

    print('Now final rois:', [roi.mz_values for roi in final_rois])

if __name__ == '__main__':
    fake_data = [
        [50, 25, 67, 80, 45, 55, 77, 61, 98, 47],
        [300, 102, 56, 73, 44, 52, 60, 80, 49, 89, 121, 54],
        [22, 69, 31, 49, 40, 20, 90],
        [54, 34, 89, 65, 45, 23, 90, 110, 53, 68],
        [67, 35, 10, 24, 45, 18, 56, 78, 43, 107],
        [67, 56, 48, 92, 81, 25, 37, 67, 34, 90, 120, 111, 78],
        [102, 54, 89, 88, 65, 59, 43, 90, 23, 26, 31],
        [67, 39, 67, 102, 67, 78, 90, 49, 89, 55, 34, 29],
        [78, 77, 56, 34, 90, 101, 24, 54, 34, 78, 43, 44],
        [99, 100, 56, 78, 98, 43, 56, 89, 45, 22, 21, 90, 34, 23, 89],
        [78, 45, 33, 29, 103, 89, 67, 87, 73, 57, 89, 83],
        [44, 89, 65, 65, 45, 34, 21, 19, 121, 55, 49, 100]
    ]

    find_rois(fake_data)