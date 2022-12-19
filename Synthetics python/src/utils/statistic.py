import matplotlib.pyplot as plt
import numpy as np
import cv2
import glob

def readTensor(path, name):
    g = glob.glob(path+ '/**/' + name, recursive=True)
    d = {}
    for f in g:
        img = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        f= f.replace(path, '')
        f= f.replace(name, '')
        f= f.replace('//', '')
        f = f.replace('\\', '')
        d[f] = img
    return d
        
def getHist(maskname, d):
    temp = np.copy(d['original'])
    temp = temp.astype(np.int)
    temp[d[maskname] == 0] = -1
    return np.histogram(temp.ravel(), bins=256, range=(0.0, 255.0), density=True)

# d = readTensor(r"F://Dissertation//Synthetic//Synthetics//Synthetics python//dataset//new","0_2022_12_15.png")


def calcSlice(path, name):
    print('calc', path, name)
    d = readTensor(path, name)
    print(d.keys())
    background = 255 - (d['vesicles'] + d['axon'] + d['PSD'] + d['mitochondria'] + d['mitochondrial_boundaries'] + d['boundaries'])
    d['background'] = background
    
    vesicles, bin_edges = getHist('vesicles', d)
    axon, bin_edges = getHist('axon', d)
    PSD, bin_edges = getHist('PSD', d)
    mitochondria, bin_edges = getHist('mitochondria', d)
    mitochondrial_boundaries, bin_edges = getHist('mitochondrial_boundaries', d)
    boundaries, bin_edges = getHist('boundaries', d)
    ground, bin_edges = getHist('background', d)

    return bin_edges, vesicles, axon, PSD, mitochondria, mitochondrial_boundaries, boundaries, ground


def printPlot(title, bin_edges, vesicles, axon, PSD, mitochondria, mitochondrial_boundaries, boundaries, ground):
    plt.title(title)
    plt.xlabel("grayscale value")
    plt.ylabel("density")
    plt.xlim([0.0, 255.0])
    plt.ylim([0.0, 0.05])
    
    
    plt.plot(bin_edges[0:-1], ground, 'g', label = 'background')
    plt.plot(bin_edges[0:-1], vesicles, 'r', label = 'vesicles')
    plt.plot(bin_edges[0:-1], axon, 'b', label = 'axon')
    plt.plot(bin_edges[0:-1], PSD, 'c', label = 'PSD')
    plt.plot(bin_edges[0:-1], mitochondria, 'm', label = 'mitochondria')
    plt.plot(bin_edges[0:-1], mitochondrial_boundaries, 'y', label = 'mitochondrial boundaries')
    plt.plot(bin_edges[0:-1], boundaries, 'k', label = 'boundaries')
    plt.legend()
    plt.show()


bin_edges, vesicles, axon, PSD, mitochondria, mitochondrial_boundaries, boundaries, ground = calcSlice(r"F://Dissertation//EPFL//new","training0000.png")
printPlot('Original layer',bin_edges, vesicles, axon, PSD, mitochondria, mitochondrial_boundaries, boundaries, ground)

path = r"F://Dissertation//Synthetic//Synthetics//Synthetics python//dataset//new"
g = glob.glob(path +"//original//*.png")

sumvesicles = np.zeros(256)
sumaxon = np.zeros(256)
sumPSD = np.zeros(256)
summitochondria = np.zeros(256)
summitochondrial_boundaries = np.zeros(256)
sumboundaries = np.zeros(256)
sumground = np.zeros(256)

for f in g:
    f = f.split('\\')[-1]
    bin_edges, vesicles, axon, PSD, mitochondria, mitochondrial_boundaries, boundaries, ground = calcSlice(path, f)
    sumvesicles = sumvesicles + vesicles
    sumaxon = sumaxon + axon
    sumPSD = sumPSD + PSD
    summitochondria = summitochondria + mitochondria
    summitochondrial_boundaries = summitochondrial_boundaries + mitochondrial_boundaries
    sumboundaries = sumboundaries + boundaries
    sumground = sumground + ground

sumvesicles = sumvesicles / len(g)
sumaxon = sumaxon / len(g)
sumPSD = sumPSD / len(g)
summitochondria = summitochondria / len(g)
summitochondrial_boundaries = summitochondrial_boundaries / len(g)
sumboundaries = sumboundaries / len(g)
sumground = sumground / len(g)

printPlot('Synthetic', bin_edges, sumvesicles, sumaxon, sumPSD, summitochondria, summitochondrial_boundaries, sumboundaries, sumground)