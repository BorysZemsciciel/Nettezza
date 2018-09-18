import sys
import nzae

sys.path.append('/nz/export/ae/applications/mypython/python2.6/site-packages/');

import numpy;
import scipy;
import sklearn;

class Hello(nzae.Ae):

    def _getFunctionResult(self, row):
        return "Hello PY ["+row[0]+"] " + " NUMPY Version: " + numpy.version.version + " SCIPY version: "+scipy.version.full_version+ " SKLEARN version: "+sklearn.__version__


Hello.run()