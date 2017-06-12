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
  

from win32com.client import Dispatch, pywintypes
import os, traceback, pdb, sys, os.path

from .utils import task_status



os.environ['PYTHONINSPECT'] = '1'
    
    
class TSX(object):
    def __init__(self,camera_support=True):
        self.oi_properties = {}
        self.oi = OI(self)
        with task_status('Connecting to the Sky X COM Interfaces'):
            try:
                self.TSX_StarChart = Dispatch("TheSkyXAdaptor.StarChart")
                self.TSX_ObjectInfo = Dispatch("TheSkyXAdaptor.ObjectInformation")
                self.TSX_Utils = Dispatch("TheSkyXAdaptor.Utils")
                self.TSX_Tele = Dispatch("TheSkyXAdaptor.RASCOMTele")
            except pywintypes.com_error as e:
                exc_info = sys.exc_info()
                if 'Invalid class string' in str(exc_info[1]):
                    print(exc_info[:2])
                    traceback.print_tb(exc_info[2])
                    print('Could not Dispatch to TheSkyX COM interface')
                    print('You may need to run TheSkyX as an administrator at least once')
                    input()
                    exit(1)
        with task_status('Connecting Telescope'):
            self.TSX_Tele.Connect()
        self.camera_support = camera_support
        if camera_support:
            with task_status('Connecting to the Sky X Camera Addon COM Interfaces'):
                try:
                    self.TSX_Camera = Dispatch("CCDSoft2XAdaptor.ccdsoft5Camera")
                    self.TSX_Image = Dispatch("CCDSoft2XAdaptor.ccdsoft5Image")
                except pywintypes.com_error as e:
                    exc_info = sys.exc_info()
                    if 'Invalid class string' in str(exc_info[1]):
                        print(exc_info[:2])
                        traceback.print_tb(exc_info[2])
                        print('Could not Dispatch to TheSkyX Camera Control COM interface')
                        print('Ensure Camera Add-on is installed; Also you may need to run TheSkyX as an administrator at least once')
                        input()
                        exit(1)
            with task_status('Connecting Camera'):
                self.TSX_Camera.Connect()
                    
        self.get_oi_properties()

    def get_oi_properties(self):
        oi = self.TSX_ObjectInfo
        self.oi_properties = {}
        for i in range(190):
            name = oi.PropertyName(i)
            self.oi_properties[name] = i
            
    def find(self,obj=None):
        if obj != None:
            with task_status('Finding object in StarChart:',obj):
                try:
                    self.TSX_StarChart.Find(obj)
                except pywintypes.com_error as e:
                    exc_info = sys.exc_info()
                    if 'Object not found' in str(exc_info[1]):
                        print('Object not found:',obj)
                        raise e
            
    def slew(self,obj=None,ra=None,dec=None):
        if obj != None:
            with task_status('Slewing to object:',obj):
                self.find(obj)
                self.TSX_Tele.SlewToRaDec(self.oi['RA (Topocentric)'],self.oi['Dec (Topocentric)'],obj)
        else:
            with task_status('Slewing to RA,Dec',ra,dec):
                self.TSX_Tele.SlewToRaDec(ra,dec,None)


    def configure_camera(self,frame=1,img_reduc=1,binning=(1,1),expo_time=30,delay=5,img_series=1):
        with task_status('Configuring camera'):
            
            if frame != None:
                self.TSX_Camera.Frame = frame
                
            if img_reduc != None:
                self.TSX_Camera.ImageReduction = img_reduc
                
            if binning != None:
                self.TSX_Camera.BinX,self.TSX_Camera.BinY = binning

            if expo_time != None:
                self.TSX_Camera.ExposureTime = expo_time
                
            if delay != None:
                self.TSX_Camera.Delay = delay
                
            if img_series != None:
                self.TSX_Camera.Series = img_series
    
    def camera_autosave(self,do_autosave=True,save_path='local/images/capture',prefix='TSX_'):
        self.TSX_Camera.AutoSaveOn = do_autosave
        self.TSX_Camera.AutoSavePath = os.path.realpath(save_path)
        self.TSX_Camera.AutoSavePrefix = prefix

            
    def sync(self,ra,dec,obj):
        with task_status('Syncing to object:','RA=',ra,'DEC=',dec,'OBJ=',obj):
            self.__MOUNT.Sync(RA,Dec,Obj)
        
    def take_image(self):
        with task_status('Taking image'):
            self.TSX_Camera.TakeImage()
    def scan_objects(self,objects,check_starchart=True):
        if isinstance(objects,basestring):
            objects = [i for i in [i.strip() for i in objects.split('\n')] if i != '']
        if check_starchart:
            with task_status('Checking existence of all objects to be scanned in StarChart'):
                for obj in objects:
                    self.find(obj)
        for obj in objects:
            self.slew(obj=obj)
            self.take_image()

class OI(object):
    def __init__(self,tsx):
        self.tsx = tsx
    def __getitem__(self,key):
        if not key in self.tsx.oi_properties:
            raise Exception('Unknown property to ObjectInformation',key)
        i = self.tsx.oi_properties[key]
        if not self.tsx.TSX_ObjectInfo.PropertyApplies(i):
            raise Exception('Unapplicable property to ObjectInformation',key)
        return self.tsx.TSX_ObjectInfo.Property(i)
        

        

    
    