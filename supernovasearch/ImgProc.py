'''
Matthew Miguel
mmiguel6288code@gmail.com
https://github.com/mmiguel6288code/super-nova-search
'''
from __future__ import absolute_import, division, print_function
from builtins import (bytes, str, open, super, range, zip, round, input, int, pow, object)
try:
  basestring
except NameError:
  basestring = str
 

import pdb
  
from .utils import task_status
    
import imreg_dft as ird
from astropy.io import fits
import matplotlib.pyplot as plt



ref = r'C:\Users\mtcym\Desktop\DT\super-nova-search\tests\test_fits\UMa_Bright.reference.NGC2841.FIT'
tgt = r'C:\Users\mtcym\Desktop\DT\super-nova-search\tests\test_fits\UMa_Bright.recent.NGC2841.FIT'


def 
 

imref = fits.open(ref)[0].data
imtgt = fits.open(tgt)[0].data
result = ird.similarity(imref,imtgt,numiter=3)
imres = result['timg']

delta = imres - imref
#ird.imshow(imref,imtgt,imres)
#plt.show()

hdu = fits.PrimaryHDU(delta)
hdu.writeto(r'C:\Users\mtcym\Desktop\DT\super-nova-search\tests\test_fits\UMa_Bright.delta.NGC2841.FIT',overwrite=True)



