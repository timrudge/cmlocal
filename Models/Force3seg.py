import random
from CellModeller.Regulation.ModuleRegulator import ModuleRegulator
from CellModeller.Biophysics.BacterialModels.CLBacterium import CLBacterium
from CellModeller.GUI import Renderers
import numpy
import math


def setup(sim):
    # Set biophysics, signalling, and regulation models
    biophys = CLBacterium(sim, jitter_z=False, max_cells=100000)

    regul = ModuleRegulator(sim, sim.moduleName)	# use this file for reg too
    # Only biophys and regulation
    sim.init(biophys, regul, None, None)

    sim.addCell(cellType=0, pos=(0,0,0))

    # Add some objects to draw the models
    therenderer = Renderers.GLBacteriumRenderer(sim)
    sim.addRenderer(therenderer)
    sim.pickleSteps = 10

def init(cell):
    cell.targetVol = 3.5 + random.uniform(0.0,0.5)
    cell.growthRate = 1.0
    cell.n_a = 1 
    cell.n_b = 1

def update(cells):
    ncells = len(cells)
    if ncells>1000:
        # Pick 
        for i in range(3):
            idx = random.uniform(0,ncells-1) 
            cell.growthRate = (gr2-gr1)*cell.n_a*0.5 + gr1
    for (id, cell) in cells.iteritems():
        cell.color = [0.1, cell.n_a/2.0, cell.n_b/2.0]
        if cell.volume > cell.targetVol:
            cell.divideFlag = True

def divide(parent, d1, d2):
    d1.targetVol = 3.5 + random.uniform(0.0,0.5)
    d2.targetVol = 3.5 + random.uniform(0.0,0.5)
