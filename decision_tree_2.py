import sys
import nzae

sys.path.append('/nz/export/ae/applications/mypython/python2.6/site-packages/');
sys.path.append('/nz/export/ae/applications/IRIS/admin/');
import sys
import numpy;
import scipy;
import sklearn;
from datetime import datetime
from sklearn import tree;
import os
from Classifier import *

# udtf do budowy klasyfikatora
# ostatnie pole jest zmienna celu



class DecisionTree(nzae.Ae):
    
    DEFAULT_REQUEST_HANDLING_STYLE = nzae.Ae.REQUEST_HANDLING_STYLE__SINGLE_THREADED;
    NZAE_REMOTE_CONNECTION_NAME  = "exampleudf";
    NZAE_REMOTE_NAME_SESSION=1;
    
    def __init__(self):
        print("_INIT_");
        self._rowId = 0;
        self.clf = Classifier()
        super(DecisionTree,self).__init__();        
        
    
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
        _str = self.debugStringVal(dt.microsecond,"time",_str);
        self._rowId += 1
        self.clf.NextRow(row);
        return self.clf.GetRowType()+ _str;
    
    def debugString(self,val,name,str):
        if (val):
            str = str + name+": true "
        else:
            str = str + name+": false"
        return str

    def debugStringVal(self,val,name,oldstr):
        return oldstr+name+"="+str(val)+" ";


DecisionTree.run()