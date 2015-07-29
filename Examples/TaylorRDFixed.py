import random
from CellModeller.Regulation.ModuleRegulator import ModuleRegulator
#from CellModeller.Biophysics.BacterialModels.CLBacterium import CLBacterium
from CellModeller.Biophysics.GeneralModels.FixedPosition import FixedPositionCL
from CellModeller.GUI import Renderers
import numpy
import math

from CellModeller.Signalling.GridDiffusion import GridDiffusion #add
from CellModeller.Integration.CLCrankNicIntegrator import CLCrankNicIntegrator #add


max_cells = 100

#Specify parameter for solving diffusion dynamics 
grid_dim = (64, 64, 12) # dimension of diffusion space, unit = number of grid
grid_size = (4, 4, 4) # grid size
grid_orig = (-128, -128, -8) # where to place the diffusion space onto simulation space


def setup(sim):
    # Set biophysics, signalling, and regulation models
    '''
    biophys = CLBacterium(sim, \
                            max_substeps=8, \
                            max_cells=max_cells, \
                            max_contacts=32, \
                            max_sqs=192**2, \
                            jitter_z=False, \
                            reg_param=2, \
                            gamma=10)
 
    # add the planes to set physical  boundaries of cell growth
    biophys.addPlane((0,-16,0), (0,1,0), 1)
    biophys.addPlane((0,16,0), (0,-1,0), 1)
    '''
    biophys = FixedPositionCL(sim, max_cells=max_cells)

    sig = GridDiffusion(sim, 2, grid_dim, grid_size, grid_orig, [7.0, 87.5])
    integ = CLCrankNicIntegrator(sim, 2, 1, max_cells, sig, boundcond='reflect')

    # use this file for reg too
    regul = ModuleRegulator(sim, sim.moduleName)	
    # Only biophys and regulation
    sim.init(biophys, regul, sig, integ)

    # Specify the initial cell and its location in the simulation
    for i in range(100):
        px = random.uniform(-100,100)
        py = random.uniform(-100,100)
        sim.addCell(cellType=0, pos=(px,py,0)) 

    # Add some objects to draw the models
#    therenderer = Renderers.GLBacteriumRenderer(sim)
#    sim.addRenderer(therenderer)
    sigrend = Renderers.GLGridRenderer(sig, integ)
    sim.addRenderer(sigrend) #Add

    sim.pickleSteps = 10



def init(cell):
    # Specify growth rate of cells
    cell.growthRate = 0

def specRateCL(): # Add
    return '''
    rates[0] = 0.f;
    '''

def sigRateCL(): #Add
    return '''
    const float fu = 0.3f;
    const float fv = -0.5f;
    const float gu = 0.5f;
    const float gv = -0.5f;

    float u = signals[0];
    float v = signals[1];
    rates[0] = 0.1f;
    rates[1] = 0.f;
    '''

#    //+ fu*u + fv*v - u*u*u;
#    //gu*u + gv*v;

def update(cells):
    #Iterate through each cell and flag cells that reach target size for division
    for (id,cell) in cells.iteritems():
        print cell.signals[0]

