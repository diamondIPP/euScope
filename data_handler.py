####################################               
# Author: Christian Dorfer
# Email: cdorfer@phys.ethz.ch                                  
####################################

from time import sleep, time
import datetime
import numpy as np
import h5py


class DataHandling(object):
     
    def __init__(self, conf):
        self.hdf = None
        self.data = None
        self.spcount = 1
        self.runnumber = self.readRunNumber()+1
        self.config = conf

    def createFile(self, comment):
        #reset old one
        self.hdf= None
        self.data = None
        self.spcount = 0
        
        #read and increase run number
        self.runnumber = self.increaseRunNumber()
        print 'Run number: ', self.runnumber
         
        #create new h5py file
        fname = 'data/run' + str(self.runnumber) + ".hdf5"
        self.hdf = h5py.File(fname, "w", libver='latest')
        self.hdf.attrs['timestamp'] = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        self.hdf.attrs['comments'] = comment
        self.data = self.hdf.create_group("data")
        self.data.attrs['nwf'] = int(self.config['DAQ']['nwf_in_burst'])
        print 'File ', fname, ' created.'
        

    def addScanPointData(self, timestamp, time_axis, wfarr):
        sp = str(self.spcount)
        self.data.create_dataset(sp, data=wfarr, compression="gzip")
        self.data[sp].attrs['timestamp'] = timestamp
        self.data[sp].attrs['time_axis'] = time_axis
        self.spcount += 1
        print 'Waveform burst ', sp, ' written to file.'
    

    def increaseRunNumber(self):
        with open('data/runnumber.dat', "r+") as f:
            runnumber = int(f.readline())
            f.seek(0)
            f.write(str(runnumber+1))
            return (runnumber+1)
            
    def readRunNumber(self):
        with open('data/runnumber.dat', "r") as f:
            return int(f.readline())
        
    def closeFile(self):
        self.hdf.flush()
        self.hdf.close()
        print 'File for run ', str(self.runnumber), ' closed.'






    
