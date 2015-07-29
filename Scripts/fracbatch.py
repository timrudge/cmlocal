import os
import sys
import subprocess
import string
import shutil

from CellModeller.Simulator import Simulator

max_cells = 10000
cell_buffer = 256

def simulate(modstr, platform, device, steps=50):
    sim = Simulator('fracbatch_var', 0.1, clPlatformNum=platform, clDeviceNum=device, moduleStr=modstr, saveOutput=True)
    sim.saveOutput=True
    while len(sim.cellStates) < max_cells-cell_buffer:
        sim.step()

def main():
    # Get module name to load
    modStringTemplate = open('Models/fracdist_var.py','rt').read()

    # Get OpenCL platform/device numbers
    if len(sys.argv)<3:
        # User input of OpenCL setup
        import pyopencl as cl
        # Platform
        platforms = cl.get_platforms()
        print "Select OpenCL platform:"
        for i in range(len(platforms)):
            print 'press '+str(i)+' for '+str(platforms[i])
        platnum = int(input('Platform Number: '))

        # Device
        devices = platforms[platnum].get_devices()
        print "Select OpenCL device:"
        for i in range(len(devices)):
            print 'press '+str(i)+' for '+str(devices[i])
        devnum = int(input('Device Number: '))
    else:
        platnum = int(sys.argv[2])
        devnum = int(sys.argv[3])

    # Set up complete, now run the simulation
    for d in range(5):
        dist = (d+5)*3 + 5
        simulate(modStringTemplate%(-dist,dist), platnum, devnum)

# Make sure we are running as a script
if __name__ == "__main__": 
    main()
