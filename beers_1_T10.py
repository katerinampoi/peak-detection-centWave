import pymzml
import matplotlib as plt
import itertools
import numpy as np

mzml_file = "data/Beer_multibeers_1_T10_POS.mzML"
run = pymzml.run.Reader(mzml_file, {2: 2e-05})

scans_MS2 = []
for spec in run:
    if spec.ms_level == 2:
        scans_MS2.append(spec.scan_time)
print(scans_MS2)
print("The number of MS2 scans is", len(scans_MS2))

#DETECTING ROIs:

rois = []
#for spec in itertools.islice(run, 200):
#Draft try
for spec in run:
    if spec.ID == 1 or len(rois) == 0:
        for mass in spec.mz:
            rois.append([mass])
    else:
        for mass in spec.mz:
            for roi in rois:
                difference = np.abs(mass - np.mean(roi))
                if difference <= 20:
                    roi.append(mass)
                else:
                    rois.append([mass])

    print(rois)





    # scan_times = []
    # ms_levels = []
    # print(
    #     "Spectrum {0}, MS level {ms_level} @ RT {scan_time:1.2f}".format(
    #         spec.ID, ms_level=spec.ms_level, scan_time=spec.scan_time_in_minutes()
    #     )
    # )
    # print(spec.mz)
    # print(spec.measured_precision)
    # scan_times.append(spec.scan_time_in_minutes())
    # ms_levels.append(spec.ms_level)
# print("Parsed {0} spectra from file {1}".format(n, mzml_file))





