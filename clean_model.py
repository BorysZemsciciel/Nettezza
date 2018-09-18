import sys
import nzae

sys.path.append('/nz/export/ae/applications/mypython/python2.6/site-packages/');
sys.path.append('/nz/export/ae/applications/IRIS/admin/');

import os
import fcntl






class DecisionTreeCleaner(nzae.Ae):
    
    DEFAULT_REQUEST_HANDLING_STYLE = nzae.Ae.REQUEST_HANDLING_STYLE__SINGLE_THREADED;
    NZAE_REMOTE_CONNECTION_NAME  = "exampleudf";
    NZAE_REMOTE_NAME_SESSION=1;
    
    TMP_MODEL_FILE = '/nz/export/ae/applications/model.pickle';
    TMP_FILE_LOCK = '/nz/export/ae/applications/training.lock';
   
        
    def SetClassifier(self,clf):
        self.clf = clf;
        
    def _runUdtf(self):
        for row in self:
            if (row[0]):
                f = open(self.TMP_FILE_LOCK,'w');
                rv = fcntl.lockf(f, fcntl.LOCK_UN)
                f.close()
                os.remove(self.TMP_MODEL_FILE);
                self.output("OK");
            else:
                self.output("use TRUE")
        
        
            
   



ae = DecisionTreeCleaner()

ae.run()