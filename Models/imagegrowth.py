import random
from CellModeller.Regulation.ModuleRegulator import ModuleRegulator
from CellModeller.Biophysics.BacterialModels.CLBacterium import CLBacterium
from CellModeller.GUI import Renderers
import numpy
import math
from PIL import Image

max_cells = 2**15
im = Image.open('/Users/timrudge/Downloads/photo-1.JPG')
imdata = im.load()


def setup(sim):
    # Set biophysics, signalling, and regulation models
    biophys = CLBacterium(sim, jitter_z=False)

    # use this file for reg too
    regul = ModuleRegulator(sim)	
    # Only biophys and regulation
    sim.init(biophys, regul, None, None)


    # Specify the initial cell and its location in the simulation
    for i in range(500):
        p = numpy.random.uniform(-50,50,(2,1))
        p = tuple(p)
        p = p + (0,)
        imcol = imdata[int(p[0]*10+1000), int(p[1]*10+1200)] 
        if max(imcol) < 128:
            d0 = random.uniform(-1,1)
            d1 = math.sqrt(1-d0*d0)
            d = (d0,d1,0)
            sim.addCell(cellType=0, pos=p, dir=d) 

    # Add some objects to draw the models
    therenderer = Renderers.GLBacteriumRenderer(sim)
    sim.addRenderer(therenderer)
    sim.pickleSteps = 1

def init(cell):
    # Specify mean and distribution of initial cell size
    cell.targetVol = 3.5 + random.uniform(0.0,0.5)
    # Specify growth rate of cells
    cell.growthRate = 1.0

def update(cells):
    #Iterate through each cell and flag cells that reach target size for division
    for (id, cell) in cells.iteritems():
        #cell.color = [cell.cellType*0.6+0.1, 1.0-cell.cellType*0.6, 0.3]
        imcol = imdata[cell.pos[0]*10+1000, cell.pos[1]*10+1200]
        cell.color = [v/255.0 for v in imcol]
        if max(cell.color)> 0.5:
            cell.growthRate = 0.0
        if cell.volume > cell.targetVol:
            cell.divideFlag = True

def divide(parent, d1, d2):
    # Specify target cell size that triggers cell division
    d1.targetVol = 2.5 + random.uniform(0.0,0.5)
    d2.targetVol = 2.5 + random.uniform(0.0,0.5)

