'''
Matthew Miguel
mmiguel6288code@gmail.com
https://github.com/mmiguel6288code/super-nova-search
'''
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import 

import TelCam_TSX

tsx = TelCam_TSX.TSX()
tsx.configure_camera(
    frame=1,
    img_reduc=1,
    binning=(1,1),
    expo_time=30,
    delay=5,
    img_series=1
    )
tsx.scan_objects('''
    NGC2976
    NGC2985
    NGC3031
    NGC3034
    NGC2768
    NGC2841
    NGC3359
    NGC3184
    NGC3077
    NGC3079
    NGC3198
    IC2574
    NGC3992
    NGC3938
    NGC3953
    NGC3631
    NGC3556
    NGC3726
    NGC3718
    NGC4605
    NGC4088
    NGC4096
    NGC5322
    NGC5585
    NGC5474
    NGC5457
''')