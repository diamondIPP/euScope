import sys
import numpy as np
import h5py

if __name__ == '__main__':
    runnumber = int(sys.argv[1])

    #open h5py file
    fname = 'run' + str(runnumber) + '.hdf5'
    print 'Opening:', fname
    hdf = h5py.File(fname, 'r')

    #group data:
    data = hdf['data']
    print 'Timestamp:', hdf.attrs['timestamp']
    print 'Comments:', hdf.attrs['comments']
    nwf = int(data.attrs['nwf'])
    print 'Number of waveforms in each readout burst:', nwf

    time_axis = data['0'].attrs['time_axis'] #use this as the time axis
    larr = len(time_axis)

    nEntries = len(data)
    print 'Number of bursts in data: ', nEntries

    for idx in range(nEntries):
        i = str(idx)
        burst_ts = data[i].attrs['timestamp']
        burst = data[i]


        for wf in range(nwf):
            wf_arr = burst[wf*larr:wf*(larr+1)]*1000 #this is the waveform in mV
            print 'Burst: ', idx, ' waveform: ', wf
            #print wf, wf_arr
    
    hdf.close()


