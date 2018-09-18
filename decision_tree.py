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
        f = open(self.TMP_FILE_LOCK,'w');
        rv = fcntl.lockf(f, fcntl.LOCK_EX)
        self.clf = self._getClassifier();
        for row in self:
            self.output(self._getFunctionResult(row)+self.model_state);
        self._storeModel(self.clf)
        rv = fcntl.lockf(f, fcntl.LOCK_UN)
        f.close()
        
            
    def _getClassifier(self):
        if os.path.isfile(self.TMP_MODEL_FILE):
            self.model_state = ' [Loaded model for dataslice] '
            return self._loadModel();
        self.model_state = ' [New one model for dataslice] '
        return Classifier();
    
    def _loadModel(self):
        with open(self.TMP_MODEL_FILE) as pickle_handle:
            return pickle.load(pickle_handle);
        
    def _storeModel(self,clf):
        with open(self.TMP_MODEL_FILE,'w') as pickle_handle:
            pickle.dump(clf, pickle_handle);
        
    def _cleanTmp(self):
        if (self.getDatasliceId()!=1):
            return;
        if os.path.isfile(self.TMP_MODEL_FILE):
            os.remove(self.TMP_MODEL_FILE);
        
    
    def _getFunctionResult(self,row):
  
        print("_ROW_");
        _str = " / ";
        _str = self.debugString(self.isRemote(),"remote",_str);
        _str = self.debugString(self.isRunningOnHost(),"host",_str);
        _str = self.debugStringVal(self.getSessionId(),"sessId",_str);
        _str = self.debugStringVal(self.getTransactionId(),"transId",_str);
        _str = self.debugStringVal(self.getDatasliceId(),"datasliceId",_str);
        _str = self.debugStringVal(self._rowId,"rowid",_str);
        _str = self.debugStringVal(os.getpid(),"pid",_str);
        _str = self.debugStringVal(id(self),"id",_str);
        dt = datetime.now()
        _str = self.debugStringVal(dt.strftime("%H-%M-%S-")+str(dt.microsecond),"time",_str);
        _str = self.debugStringVal(os.path.dirname(__file__), "pwd",_str);
        self._rowId += 1
      
        self.clf.NextRow(row);
        return self.clf.GetRowType();
    
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