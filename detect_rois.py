import pymzml
import matplotlib as plt
import itertools
import numpy as np
from roi_handler import ROI

mzml_file = "data/Beer_multibeers_5_T10_POS.mzML"
# run = pymzml.run.Reader(mzml_file)


def find_rois(run):
    # Initialization - Add the first m/z in the rois list
    rois = []
    final_rois = []
    max_difference = 20
    p_min = 15
    for spec in run:
        # print("Now checking:", spec.ID)
        if len(rois) == 0:
            for mass in spec:
                roi = ROI(mz_values=[mass])
                rois.append(roi)
    # For current scan, add m/z to roi in rois, depending on the mass value
        else:
            waiting_rois = []       # m/z from current scan that didn't meet the condition in line 27 are added in this list
            for mass in spec:
                print("Now checking mass:", mass)
                mass_added = False
                for roi in rois:
                    print("Now checking roi:", roi.mz_values, roi.extended)
                    difference = np.abs(mass - np.mean(roi.mz_values))
                    if difference <= max_difference:
                        roi.mz_values.append(mass)
                        roi.extended = True
                        print("mass added")
                        mass_added = True
                        break

                if not mass_added:
                    waiting_rois.append(ROI(mz_values=[mass]))
            for roi in rois:
                if not roi.extended:
                    if len(roi.mz_values) < p_min:
                        print('Now removing roi:', roi.mz_values)
                        rois.remove(roi)
                    elif len(roi.mz_values) >= p_min:
                        print('Now adding roi:', roi.mz_values)
                        final_rois.append(roi)

            # if len(roi) == initial_len:     # Check if rois are extended to the next step, based on the roi's length
            #     if len(roi) < p_min:        # Remove the rois not extended and containing less than p_min centroids
            #         print('Now removing roi:', roi)
            #         rois.remove(roi)
            #     elif len(roi) >= p_min:     # Keep the rois not extended and containing at least p_min centroids
            #         final_rois.append(roi)
            #         print("ROI found")
            #         rois.remove(roi)
            #     print("Now rois after:", rois)
            print('Waiting rois now: ', [roi.mz_values for roi in waiting_rois])
            rois.extend(list(waiting_rois))         # Merge waiting list and rois list

    print('Now final rois:', [roi.mz_values for roi in final_rois])

if __name__ == '__main__':
    fake_data = [
        [50, 55, 61],
        [52, 60, 80, 49],
        [40, 20, 90]
    ]
    find_rois(fake_data)