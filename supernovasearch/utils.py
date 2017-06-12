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
  
from contextlib import contextmanager
import time

verbose = True
@contextmanager
def task_status(*status):
    status = ' '.join(str(s) for s in status)
    t = time.time()
    if verbose:
        print('Start:',status+'...')
    yield
    if verbose:
        print('  Done:',status,';','%0.3f' % (time.time()-t),'seconds')