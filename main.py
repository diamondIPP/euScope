####################################               
# Author: Christian Dorfer
# Email: cdorfer@phys.ethz.ch                                  
####################################

import sys
from time import time
from configobj import ConfigObj
from tektronix import TektronixMSO5204B
from data_handler import DataHandling


    
if __name__ == '__main__':

    config = ConfigObj('config.ini')
    
    dh = DataHandling(config)
    dh.createFile("Test readout program for the MSO5204B at PSI")

    tek = TektronixMSO5204B(config)
    tek.open()
    tek.configure()

    bursts = int(config['DAQ']['bursts'])
    
    for idx in range(bursts):
        (scaleddata, scaledtime) = tek.acquireWaveforms()
        timestamp = time()
        dh.addScanPointData(timestamp, scaledtime, scaleddata)

    dh.closeFile()
    tek.close()
