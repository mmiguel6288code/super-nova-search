import sys
from supernovasearch import utils
utils.verbose = True
run = sys.argv[1:]

if len(run) == 0 or '1' in run:
    with utils.task_status('Unit Test 1: Test Telcam'):
        from tests import test_telcam
if len(run) == 0 or '2' in run:
    with utils.task_status('Unit Test 2: Test ImgProc'):
        from tests import test_imgproc