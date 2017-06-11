'''
Matthew Miguel
mmiguel6288code@gmail.com
https://github.com/mmiguel6288code/super-nova-search
'''
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import 

from astropy.io import fits
from PIL import Image
from matplotlib import pyplot as mpl

# chose your color map from Matplotlib
cmap = mpl.cm.gist_heat
# load your image
im = fits.getdata('image.fits')
# apply image scaling here, the end product should be an image with
# values ranging from 0 to 255
im = ...
# convert to a PIL image, generate the RGB values, combine, then save
pim = Image.fromarray(im.astype(uint8))
r = pim.point(lambda x: cmap(x/255.0)[0] * 255)
g = pim.point(lambda x: cmap(x/255.0)[1] * 255)
b = pim.point(lambda x: cmap(x/255.0)[2] * 255)
pim = Image.merge("RGB", (r, g, b))
pim.save('image.png')
