#This is a exemple of the scripts used in the article "Large‐scale genetic 
##panmixia in the blue shark (Prionace glauca): A single worldwide population, 
##or a genetic lag‐time effect of the “grey zone” of differentiation?" to
##determine the existence and duration of the grey zone.

#written by Diane Bailleul, with the help of Bo Peng and Solenn Stoeckel.
#email: diane.bailleul.pro@gmail.com

#Please, do not use (with or witout modifications) without citing
##SimuPop and the original article.

#############################################################################
#Fst computation with migration, with m = 1/10000 and Nm = 10 and N = 100000#
#############################################################################

import simuPOP as sim
import numpy as np
import os
import time

from simuPOP.sampling import drawRandomSample

global NOM
NOM = time.strftime('%Y-%m-%d-%Hh %Mmin',time.localtime())
print NOM

global CHEMIN
CHEMIN = os.getcwd()
print CHEMIN

def reccord (chaine,nfic):
    cheminfst = os.path.join(CHEMIN, (NOM + nfic + '.txt'))
    resultsfst=open(cheminfst,'a')
    resultsfst.write(chaine)
    resultsfst.close
    return cheminfst

def calcFst(pop):
    sortie = ''
    sim.stat(pop, structure=range(10), vars=['F_st'])
    Fstpop = pop.dvars().F_st
    for a in range(100):
        sample = drawRandomSample(pop, sizes=[50]*2)
        sim.stat(sample, structure=range(10), vars=['F_st'])
        Fstsample = sample.dvars().F_st
        sample.addInfoFields('order')
        order = list(range(100))
        fstsim = ''
        for rep in range(1000):
            merged=sample
            merged.mergeSubPops()
            np.random.shuffle(order)
            merged.setIndInfo(order, field = 'order')
            merged.sortIndividuals('order')
            merged.splitSubPop(0, [50]*2)
            sim.stat(merged, structure=range(10), vars=['F_st'])
            fstsim += '%s\t' % merged.dvars().F_st
        sortie += '%3d\t%.6f\t%3d\t%.6f\t%s\n' % (pop.dvars().gen, Fstpop, a, Fstsample, fstsim)
    reccord (sortie, "dataout")
    return True

    
pop = sim.Population([100000]*2, loci=[10]*10, infoFields='migrate_to')   
    
pop.evolve(
initOps=[
sim.InitSex(),
sim.InitGenotype(freq=[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1])
],
preOps=sim.Migrator(rate=[
    [0,0.0001],
    [0.0001,0]
    ],
mode=sim.BY_PROPORTION),
matingScheme=sim.RandomMating(ops=sim.Recombinator(rates=0.01)),
postOps=[
sim.PyOperator(func=calcFst, step=50)
],
gen = 5000
)
