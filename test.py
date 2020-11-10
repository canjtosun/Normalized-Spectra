import norm_Sean_v20181029 as normalization
import utility_functions
import time
import difflib

STARTS_FROM, ENDS_AT = 0, 9
LOG_FILE = "log.txt"
normalization.clear_file(LOG_FILE)
normalization.normalize_spectra(STARTS_FROM, ENDS_AT)

expected_results = "new_correct_output.txt"

with open(expected_results, 'r') as file1:
    with open(LOG_FILE, 'r') as file2:
        diff = difflib.unified_diff(
            file1.readlines(),
            file2.readlines(),
            fromfile=expected_results,
            tofile=LOG_FILE,
        )
        _empty = object()
        if next(diff, _empty) == _empty:
            print("Test passed, outputs are identical!")
        else:
            for line in diff:
                print(line)


