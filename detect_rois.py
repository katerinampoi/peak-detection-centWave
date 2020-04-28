import pymzml
import matplotlib as plt
import itertools as it
import numpy as np
from roi_handler import ROI
from bisect import bisect_left

mzml_file = " "
# run = pymzml.run.Reader(mzml_file)

def find_rois(run):
    rois = []
    final_rois = []
    max_difference = 20
    p_min = 5

    # Initialization
    for spec in run:
        if len(rois) == 0:
            for mass in spec:
                roi = ROI(mz_values=[mass])
                rois.append(roi)

        else:
            for roi in rois:
                roi.set_extended(False)
            # Mass not been matched is temporarily added here
            waiting_rois = []
            print("--------Scan ends here--------")
            print("Rois now:", [roi.get_mz_values() for roi in rois])
            for mass in spec:
                mass_added = False
                print("Now checking mass:", mass)
                # Rois are sorted according to ROI(mz_values) mean
                rois.sort(key=lambda x: x.get_mz_mean())

                actual_index = bisect_left(rois, mass)
                print("Bisect shows index:", actual_index)
                difference_1 = np.abs(mass - rois[actual_index - 1].get_mz_mean())

                if actual_index == len(rois):
                    if difference_1 < max_difference:
                        rois[actual_index - 1].add_mz_value(mass)
                        rois[actual_index - 1].update_mz_mean()
                        rois[actual_index - 1].set_extended(True)
                        print("mass added")
                        mass_added = True
                    else:
                        waiting_rois.append(ROI(mz_values=[mass]))
                        print("mass added to waiting rois")
                else:
                    difference_2 = np.abs(mass - rois[actual_index].get_mz_mean())
                    if difference_1 < difference_2:
                        index_to_look = actual_index - 1
                        min_diff = difference_1
                    else:
                        index_to_look = actual_index
                        min_diff = difference_2

                    if min_diff < max_difference:
                        print('Min diff', min_diff)
                        rois[index_to_look].add_mz_value(mass)
                        rois[index_to_look].add_mz_value(mass)
                        rois[index_to_look].set_extended(True)
                        print("mass added")
                        mass_added = True
                    else:
                        waiting_rois.append(ROI(mz_values=[mass]))

            for roi in rois:
                print("Rois formed in this scan:", roi.get_mz_values())
                print("roi extended:", roi.get_extended())
                # Finding final rois
                if roi.get_extended() is False:
                    if len(roi.get_mz_values()) >= p_min:
                        print('Adding roi to final_rois:', roi.get_mz_values())
                        final_rois.append(roi)
                # Keeping rois that have been extended
            rois = list(it.filterfalse(lambda x: not x.get_extended(), rois))
            print("Rois kept after scan ends:", [roi.get_mz_values() for roi in rois])
            rois.extend(list(waiting_rois))

    print('Final rois:', [roi.get_mz_values() for roi in final_rois])


if __name__ == '__main__':
    fake_data = [
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
        [44, 89, 65, 65, 45, 34, 21, 19, 121, 55, 49, 100], [400]
    ]

    find_rois(fake_data)

