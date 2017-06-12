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
 

import pdb, os, re, datetime
  
from .utils import task_status
    
import imreg_dft as ird
from astropy.io import fits
import matplotlib.pyplot as plt

capture_path = r'local/images/capture'
reference_path = r'local/images/reference'
delta_path = r'local/images/delta'


def today_mdy():
    return datetime.datetime.now().strftime('%B %d %Y')
    
def valid_mdy(mdy):
    m = re.search('([A-Za-z]+) (\\d+) (\\d+)',mdy)
    if m == None:
        return False
    month,day,year = m.groups()
    
    
    if not month in ['January','February','March','April','May','June','July','August','September','October','November','December']:
        return False
    if not(1 <= int(day) <= 31):
        return False
    return True
     

def parse_fits_name(fname):
    '<prefix>.<img_number>.<object_name>.fit'
    m = re.search('(.+)\\.([0-9]{8})\\.(.+)\\.fit',fname,re.I)
    if m != None:
        prefix,img_num,obj_name = m.groups()
    else:
        prefix,img_num,obj_name = None,None,None
    return prefix,img_num,obj_name
    
def make_fits_name(prefix,img_num,obj_name):
    return prefix + '.' + img_num + '.' + obj_name + '.FIT'

def reference_fits_name(fname):
    prefix,_,obj_name = parse_fits_name(fname)
    
    return make_fits_name(prefix,'reference',obj_name)
    

def load_fits_data(fpath):
    return fits.open(fpath)[0].data
def similarity(imref,imtgt):
    return ird.similarity(imref,imtgt,numiter=3)['timg']
def save_fits_data(imdata,fpath):
    hdu = fits.PrimaryHDU(imdata)
    hdu.writeto(fpath,overwrite=True)
def find_unprocessed_captures(mdy):
    '''
        mdy = <Month> <Day> <Year>
        e.g. June 11 2017
    '''
    to_process = []
    with task_status('Finding unprocessed captures'):
        for fname in os.listdir(os.path.join(capture_path,mdy)):
            if not os.path.exists(os.path.join(delta_path,mdy,fname)):
                ref_name = reference_fits_name(fname)
                if not os.path.exists(os.path.join(reference_path,ref_name)):
                    raise Exception('Missing reference file',ref_name)
                to_process.append(fname)
    return to_process
    
def process_images(mdy=None):
    if mdy == None:
        mdy = today_mdy()
    if not valid_mdy(mdy):
        raise Exception('Invalid date folder name:',mdy)
    to_process = find_unprocessed_captures(mdy)
    for fname in to_process:
        capture_fpath = os.path.join(capture_path,mdy,fname)
        ref_name = reference_fits_name(fname)
        ref_fpath = os.path.join(reference_path,ref_name)
        delta_fpath = os.path.realpath(os.path.join(delta_path,mdy,fname))
        
        with task_status('Loading captured file:',fname):
            imcap = load_fits_data(capture_fpath)
        with task_status('Loading reference file:',ref_name):
            imref = load_fits_data(ref_fpath)
        with task_status('Performing image registration'):
            imreg = similarity(imref,imcap)
        with task_status('Performing delta'):
            imdel = imreg - imref
        with task_status('Saving delta'):
            os.makedirs(os.path.join(delta_path,mdy),exist_ok=True)
            save_fits_data(imdel,delta_fpath)
        
    
    



