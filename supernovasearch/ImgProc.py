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
from shutil import copyfile
  
from .utils import task_status
    
import imreg_dft as ird
from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from photutils import DAOStarFinder

import matplotlib.pyplot as plt
from astropy.visualization import SqrtStretch
from astropy.visualization.mpl_normalize import ImageNormalize
from photutils import CircularAperture
import matplotlib.pyplot as plt


capture_path = r'local/images/capture'
reference_path = r'local/images/reference'
delta_path = r'local/images/delta'
log_path = r'local/detection_logs/'

def make_mdy(y,m,d):
    return datetime.datetime(y,m,d).strftime('%B %d %Y')
    
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
                try:
                    ref_name = reference_fits_name(fname)
                except:
                    print('Cannot determine reference file for file:',fname)
                else:
                    if not os.path.exists(os.path.join(reference_path,ref_name)):
                        raise Exception('Missing reference file',ref_name)
                    to_process.append(fname)
    return to_process

    
    
def source_detection(imdata):
    mean,median,std = sigma_clipped_stats(imdata,sigma=3.0,iters=5)
    daofind = DAOStarFinder(fwhm=3.0,threshold=5.*std)
    sources = daofind(imdata - median)
    sources.sort('flux')
    sources.reverse()
    return sources
    
def supernova_detection(imdel,imref):
    refmean,refmedian,refstd = sigma_clipped_stats(imref,sigma=3.0,iters=5)
    mean,median,std = sigma_clipped_stats(imdel,sigma=3.0,iters=5)
    daofind = DAOStarFinder(fwhm=3.0,threshold=5.*refstd)
    sources = daofind(imdel - median)
    sources.sort('flux')
    sources.reverse()
    return sources

def save_source_log(mdy,cap_fname,sources,ref=False):
    os.makedirs(os.path.join(log_path,mdy),exist_ok=True)
    prefix,_,obj_name = parse_fits_name(cap_fname)
    if ref:
        log_fpath = os.path.join(log_path,mdy,prefix + '.' + obj_name + '.ref.log')
    else:
        log_fpath = os.path.join(log_path,mdy,prefix + '.' + obj_name + '.log')
    sources.write(log_fpath,format='ascii.ecsv',overwrite=True)
    #with open(log_fpath,'w') as f:
    #    f.write(str(sources))
    
def save_source_plot(mdy,cap_fname,sources,im_data,ref=False):
    os.makedirs(os.path.join(log_path,mdy),exist_ok=True)
    positions = (sources['xcentroid'],sources['ycentroid'])
    apertures = CircularAperture(positions,r=4.)
    norm = ImageNormalize(stretch=SqrtStretch())
    plt.figure()
    apertures.plot(color='blue',lw=1.5,alpha=0.5)
    plt.imshow(im_data,cmap='Greys',origin='lower',norm=norm)
    prefix,_,obj_name = parse_fits_name(cap_fname)
    if ref:
        plot_fpath = os.path.join(log_path,mdy,prefix + '.' + obj_name + '.ref.png')
    else:
        plot_fpath = os.path.join(log_path,mdy,prefix + '.' + obj_name + '.png')
    plt.savefig(plot_fpath)
    plt.close()
    

def copy_to_reference(y=None,m=None,d=None,mdy=None):
    if y == None:
        if mdy == None:
            mdy = today_mdy()
    else:
        mdy = make_mdy(y,m,d)
    if not valid_mdy(mdy):
        raise Exception('Invalid date folder name:',mdy)
    cap_path = os.path.join(capture_path,mdy)
    
    with task_status('Copying files to reference:',mdy):
        for fname in sorted(os.listdir(cap_path)):
            capture_fpath = os.path.join(capture_path,mdy,fname)
            ref_name = reference_fits_name(fname)
            ref_fpath = os.path.join(reference_path,ref_name)
            with task_status('Copying',fname):
                copyfile(capture_fpath,ref_fpath)
        
        
def process_images(y=None,m=None,d=None,mdy=None):
    if y == None:
        if mdy == None:
            mdy = today_mdy()
    else:
        mdy = make_mdy(y,m,d)
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
        with task_status('Performing source detection'):
            sources = supernova_detection(imdel,imref)
            refsources = source_detection(imref)
            
        with task_status('Saving source detection results'):
            save_source_log(mdy,fname,sources)
            save_source_log(mdy,fname,refsources,ref=True)
            save_source_plot(mdy,fname,sources,imreg)
            save_source_plot(mdy,fname,refsources,imref,ref=True)
        
        
    

    



