# super-nova-search

Looking for supernovas in the night sky

![NGC2841 (no post-processing)](images/NGC2841.png)

## Software Components

### Software Environment
- [Anaconda 2 or 3](https://www.continuum.io/downloads)
  - If using python 2, may need to "pip install future"
  
- [The Sky X with TPoint and Camera Add-Ons](http://www.bisque.com/sc/pages/TheSkyX-Professional-Edition.aspx)

### Telescope and Camera Control
TelCam_TSX.py: General functionalities to perform Telescope and Camera Control

Example usage: Scanning a set of targets
```python
from supernovasearch.TelCam_TSX import TSX

t = TSX()
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
    save_path='local/images/capture',
    prefix='test_telcam'
)

tsx.scan_objects('''
    Mars
    NGC2985
    Regulus
''')
```

![Telescope and Camera Control Flowchart](Flowcharts/TelCam%20Flowchart.png)

### Image Processing

ImgProc.py: General functionalities to perform image processing

Example Usage: Creating reference images
```python
#First scan desired targets using TelCam_TSX
#Then do:

from supernovasearch.ImgProc import copy_to_reference
copy_to_reference(2017,6,11) #leave arguments empty for current date
```

Example Usage: Supernova Search image processing
```python
#First create reference images
#Then do:
from supernovasearch.ImgProc import process_images
process_images(2017,6,11) #leave arguments empty for current date
```

![Image Processing Flowchart](Flowcharts/ImgProc%20Flowchart.png)

Filename/Folder structure:
  * `FITS file name structure (capture or delta): <prefix>.<img_number>.<object_name>.fit`
  * `FITS file name structure (reference): <prefix>.reference.<object_name>.fit`
  * Folder Structure:
    * `local/images/reference/<fits files>`
    * `local/images/capture/<Month-Day-Year>/<fits files>`
    * `local/images/delta/<Month-Day-Year>/<fits files>`
    * `local/detection_logs/<Month-Day-Year>/<log files>`

Image Registration performed via [imreg_dft](https://pypi.python.org/pypi/imreg_dft/)

Source Detection performed via [photutils.detection](http://photutils.readthedocs.io/en/stable/photutils/detection.html) (DAOStarFinder)
    
  


