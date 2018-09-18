import sys
import nzae

sys.path.append('/nz/export/ae/applications/mypython/python2.6/site-packages/');
sys.path.append('/nz/export/ae/applications/IRIS/admin/');


from datetime import datetime
import os
import fcntl
from Classifier import *
import cPickle as pickle

# udtf do budowy klasyfikatora
# ostatnie pole jest zmienna celu


class ModelError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class DecisionTree(nzae.Ae):
    
    DEFAULT_REQUEST_HANDLING_STYLE = nzae.Ae.REQUEST_HANDLING_STYLE__SINGLE_THREADED;
    NZAE_REMOTE_CONNECTION_NAME  = "exampleudf";
    NZAE_REMOTE_NAME_SESSION=1;
    
    TMP_MODEL_FILE = '/nz/export/ae/applications/model.pickle';
    TMP_FILE_LOCK = '/nz/export/ae/applications/training.lock';
    
    def __init__(self):
        print("_INIT_");
        self._rowId = 0;
        self.clf = False;
        super(DecisionTree,self).__init__();       
        self.model_state = 'Created';
        
    def SetClassifier(self,clf):
        self.clf = clf;
        
    def _runUdtf(self):
        self.clf = self._getClassifier();
        for row in self:
            self.output(self._getFunctionResult(row));        
        
            
    def _getClassifier(self):
        if os.path.isfile(self.TMP_MODEL_FILE):
            return self._loadModel();
        raise ModelError("Brak wytrenowanego modelu predykcji")
    
    def _loadModel(self):
        with open(self.TMP_MODEL_FILE) as pickle_handle:
            return pickle.load(pickle_handle);
        
    
    def _getFunctionResult(self,row):
        return self.clf.PredictRow(row);
        
    
    def debugString(self,val,name,str):
        if (val):
            str = str + name+": true "
        else:
            str = str + name+": false "
        return str

    def debugStringVal(self,val,name,oldstr):
        return oldstr+name+"="+str(val)+" ";



ae = DecisionTree()

ae.run()