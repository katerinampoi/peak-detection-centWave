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

    # Initialization
    for spec in run:
        if len(rois) == 0:
            for mass in spec:
                roi = ROI(mz_values=[mass])
                rois.append(roi)

        else:
            for roi in rois:
                roi.set_extended(False)                      # for every new scan, roi is taken as not extended
            waiting_rois = []                                # masses not added in any roi temporarily added here
            for mass in spec:
                mass_added = False
                print("Now checking mass:", mass)
                rois.sort(key=lambda x: x.get_mz_mean())     # rois are sorted according to ROI(mz_values) mean
                for roi in rois:
                    print("Now checking roi:", roi.get_mz_values(), roi.get_extended())
                    difference = np.abs(mass - roi.get_mz_mean())
                    if difference <= max_difference:
                        roi.add_mz_value(mass)
                        roi.update_mz_mean()
                        roi.set_extended(True)
                        print("mass added")
                        mass_added = True
                        break

                if not mass_added:
                    waiting_rois.append(ROI(mz_values=[mass]))
                    print("Waiting rois:", [roi.get_mz_values() for roi in waiting_rois])
            for roi in rois:
                if not roi.get_extended():
                    if len(roi.get_mz_values()) < p_min:
                        print('Removing roi:', roi.get_mz_values())
                        rois.remove(roi)
                    elif len(roi.get_mz_values()) >= p_min:
                        print('Adding roi to final_rois:', roi.get_mz_values())
                        final_rois.append(roi)

            rois.extend(list(waiting_rois))

    print('Final rois:', [roi.get_mz_values() for roi in final_rois])


if __name__ == '__main__':
    fake_data = [
        [],
        [50, 25, 67, 80, 45, 55, 77, 61, 98, 47],
        [300, 102, 56, 73, 44, 52, 60, 80, 49, 89, 121, 54],
        [22, 69, 31, 49, 40, 20, 90],
        [54, 34, 89, 65, 45, 23, 90, 110, 53, 68],
        [67, 35, 10, 24, 310, 45, 18, 56, 78, 43, 107],
        [67, 56, 48, 92, 81, 25, 37, 67, 34, 90, 120, 111, 78],
        [102, 54, 89, 88, 65, 59, 43, 90, 23, 26, 31],
        [67, 39, 67, 102, 67, 78, 90, 49, 89, 55, 34, 29],
        [78, 77, 56, 34, 90, 101, 24, 54, 34, 78, 43, 44],
        [99, 100, 56, 78, 98, 43, 56, 89, 45, 22, 21, 90, 34, 23, 89],
        [78, 45, 33, 29, 103, 89, 67, 87, 73, 57, 89, 83],
        [44, 89, 65, 65, 45, 34, 21, 19, 121, 55, 49, 100]
    ]

    find_rois(fake_data)