import random
from CellModeller.Regulation.ModuleRegulator import ModuleRegulator
from CellModeller.Biophysics.BacterialModels.CLBacterium import CLBacterium
from CellModeller.GUI import Renderers
import numpy
import math

max_cells = 10000
rodlen = 3.5
cols = {0:[0.5,0.3,0.3], 1:[0.3,0.3,0.5]}

def setup(sim):
    # Set biophysics, signalling, and regulation models
    biophys = CLBacterium(sim, jitter_z=False, max_planes=9)

    sim.dt = 0.025
    #biophys.addPlane((0,0,-0.5), (0,0,1), 1.0)
    #biophys.addPlane((0,0,0.5), (0,0,-1), math.sqrt(7.5e-4))

    angs = [i*math.pi/4 for i in range(8)]
    for a in angs:
        x = math.cos(a)
        y = math.sin(a)
        p = (50*x,50*y,0)
        n = (-x,-y,0)
        biophys.addPlane(p,n, 1.0)

    regul = ModuleRegulator(sim)	# use this file for reg too
    # Only biophys and regulation
    sim.init(biophys, regul, None, None)

    #ct = 0
    #for x in range(-4,5):
    #    for y in range(-4,5):
    sim.addCell(cellType=0, pos=(0,-10,0), color=(1,0,0)) #x*40,y*40,0))
    sim.addCell(cellType=1, pos=(0,10,0), color=(0,0,1)) #x*40,y*40,0))
    #        ct += 1
    #sim.addCell(cellType=1, pos=(20,0,0))


    # Add some objects to draw the models
    therenderer = Renderers.GLBacteriumRenderer(sim)
    sim.addRenderer(therenderer)
    sim.pickleSteps = 1

def init(cell):
    cell.targetVol = rodlen + random.uniform(0.0,0.5)
    cell.growthRate = 1.0
    cell.color = cols[cell.cellType]

def update(cells):
    for (id, cell) in cells.iteritems():
        if cell.volume > cell.targetVol:
            cell.divideFlag = True

def divide(parent, d1, d2):
    d1.targetVol = rodlen + random.uniform(0.0,0.5)
    d2.targetVol = rodlen + random.uniform(0.0,0.5)
    u1 = numpy.random.uniform(-1.0,1.0,size=(3,))
    u2 = numpy.ones((3,)) - u1
    d1.color = [parent.color[i] + 0.1*u1[i] for i in range(3)]

