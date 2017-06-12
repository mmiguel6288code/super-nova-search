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

Example usage:
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

![Image Processing Flowchart](Flowcharts/ImgProc%20Flowchart.png)

Filename/Folder structure:
  * FITS file name structure: <prefix>.<img_number>.<object_name>.fit
  * Folder Structure:
    * local/images/reference/<fits files>
    * local/images/capture/<Month-Day-Year>/<fits files>
    * local/images/delta/<Month-Day-Year>/<fits files>
    
  


