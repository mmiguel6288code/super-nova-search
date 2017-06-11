# super-nova-search

Looking for supernovas in the night sky

![NGC2841 (no post-processing)](images/NGC2841.png)

## Software Components

### Software Environment
- [Anaconda 2 or 3](https://www.continuum.io/downloads)
- [The Sky X with TPoint and Camera Add-Ons](http://www.bisque.com/sc/pages/TheSkyX-Professional-Edition.aspx)

### Telescope and Camera Control
TelCam_TSX.py: General functionalities to perform Telescope and Camera Control

Example usage:
```python
from TelCam_TSX import TSX

t = TSX()
tsx.configure_camera(
    frame=1,
    img_reduc=1,
    binning=(1,1),
    expo_time=30,
    delay=5,
    img_series=1
    )
tsx.scan_objects('''
    Mars
    NGC2985
    Regulus
''')
```
![Telescope and Camera Control](Flowcharts/TelCam%20Flowchart.png)


### Image Processing


