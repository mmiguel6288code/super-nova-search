'''
Matthew Miguel
mmiguel6288code@gmail.com
https://github.com/mmiguel6288code/super-nova-search
'''
from __future__ import absolute_import, division, print_function
from builtins import (bytes, str, open, super, range, zip, round, input, int, pow, object)   

from .context import supernovasearch

tsx = supernovasearch.TelCam_TSX.TSX()
tsx.configure_camera(
    frame=1,
    img_reduc=1,
    binning=(1,1),
    expo_time=1,
    delay=1,
    img_series=1
    )
    
tsx.camera_autosave(
    do_autosave=True,
    save_path='local/images',
    prefix='test_telcam_'
)

tsx.scan_objects('''
    Mars
    NGC2985
    Regulus
''')
