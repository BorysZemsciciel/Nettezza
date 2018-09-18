#!/usr/bin/env python2
#encoding: UTF-8
from vendor.HoeffdingTree.hoeffdingtree import *

class Classifier(object):
    def __init__(self, grace_period=50, h_tie_threshold=0.05, split_confidence=0.0001, minimum_fraction_of_weight_info_gain=0.01, probe=10):
        self.probe_instances = []
        self.headers = []
        self.att_values = []
        self.vfdt = HoeffdingTree()
        self.vfdt.set_grace_period(grace_period)
        self.vfdt.set_hoeffding_tie_threshold(h_tie_threshold)
        self.vfdt.set_split_confidence(split_confidence)
        self.vfdt.set_minimum_fraction_of_weight_info_gain(minimum_fraction_of_weight_info_gain)
        self._row_type = 'Training';
        self.index = 0;
        self.probe = probe;
        self.dataset = False;
        self.class_index = 0;

    def generateHeaders(self, noColumns):
        headers = []
        for i in range(noColumns-1):
            headers.append("prop" + str(i));
        headers.append("class");
        return headers

        
    
    
                
            
    def NextRow(self, row):
        self._row_type = "Training ";
        if (self.index == 0):
            self.headers = self.generateHeaders(len(row));
            self.class_index = len(row)-1
            self.att_values = [[] for i in range(len(self.headers))];
            self._row_type = 'Probe '+str(self.index)
        if (self.index < self.probe):
            self._row_type = "Probe "
            self.probeRow(row)
        if (self.index >= self.probe):
            if (self.index == self.probe):
                self.trainProbe()
                self._row_type = 'Last Probe '
            self.trainRow(row)
        self.index = self.index + 1;
        
        
    def PredictRow(self, row):
        new_instance = self.row2instance(row)
        new_instance.set_dataset(self.dataset)
        result = self.vfdt.distribution_for_instance(new_instance);
        return '/'.join([str(i) for i in result]);
        
            
    def probeRow(self, row):
        inst = list(row)
        self.probe_instances.append(inst);
        for j in range(len(self.headers)):
            try:
                inst[j] = float(inst[j])
                self.att_values[j] = None
            except ValueError:
                inst[j] = str(inst[j])
            if isinstance(inst[j], str):
                if self.att_values[j] is not None:
                    if inst[j] not in self.att_values[j]:
                        self.att_values[j].append(inst[j])
                else:
                    raise ValueError(
                                     'Attribute {0} has both Numeric and Nominal values.'
                                     .format(self.headers[j]))
    
    def trainProbe(self):
        self.dataset = self.prepareDataset()
        self.vfdt.build_classifier(self.dataset)
        pass
    
    def prepareDataset(self):
        attributes = []
        for i in range(len(self.headers)):
            if self.att_values[i] is None:
                attributes.append(Attribute(str(self.headers[i]), att_type='Numeric'))
            else:
                attributes.append(Attribute(str(self.headers[i]), self.att_values[i], 'Nominal'))
  
        dataset = Dataset(attributes, self.class_index)
        for inst in self.probe_instances:
            for i in range(len(self.headers)):
                if attributes[i].type() == 'Nominal':
                    inst[i] = int(attributes[i].index_of_value(str(inst[i])))
            dataset.add(Instance(att_values=inst))
        self.attributes = attributes;
        return dataset
    
    def row2instance(self,row):
        inst_values = list(row)
        for i in range(len(inst_values)):
            if self.dataset.attribute(index=i).type() == 'Nominal':
                inst_values[i] = int(self.dataset.attribute(index=i)
                                     .index_of_value(str(inst_values[i])))
            else:
                inst_values[i] = float(inst_values[i])

        return Instance(att_values=inst_values)
    
    def trainRow(self, row):
        new_instance = self.row2instance(row)
        new_instance.set_dataset(self.dataset)
        self.vfdt.update_classifier(new_instance)
        pass
        
        
    def DebugString(self):
        return "Debug"
    
    def GetRowType(self):
        return self._row_type;