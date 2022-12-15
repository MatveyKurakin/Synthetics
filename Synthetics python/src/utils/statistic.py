import matplotlib.pyplot as plt
import numpy as np
import cv2
import glob

def readTensor(path, name):
    print(path + '**' + name)
    g = glob.glob(path+ '/**/' + name, recursive=True)
    print(g)
    d = {}
    for f in g:
        img = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        f= f.replace(path, '')
        f= f.replace(name, '')
        f= f.replace('//', '')
        f = f.replace('\\', '')
        d[f] = img
    return d
        
def getHist(maskname):
    temp = np.copy(d['original'])
    temp = temp.astype(np.int)
    temp[d[maskname] == 0] = -1
    return np.histogram(temp.ravel(), bins=256, range=(0.0, 255.0), density=True)

d = readTensor(r"F://Dissertation//Synthetic//Synthetics//Synthetics python//dataset//new","0_2022_12_15.png")
# d = readTensor(r"F://Dissertation//EPFL//new","training0000.png")

background = 255 - (d['vesicles'] + d['axon'] + d['PSD'] + d['mitochondria'] + d['mitochondrial_boundaries'] + d['boundaries'])
d['background'] = background

vesicles, bin_edges = getHist('vesicles')
axon, bin_edges = getHist('axon')
PSD, bin_edges = getHist('PSD')
mitochondria, bin_edges = getHist('mitochondria')
mitochondrial_boundaries, bin_edges = getHist('mitochondrial_boundaries')
boundaries, bin_edges = getHist('boundaries')
ground, bin_edges = getHist('background')

plt.title("Layer Histogram")
plt.xlabel("grayscale value")
plt.ylabel("density")
plt.xlim([0.0, 255.0])


plt.plot(bin_edges[0:-1], ground, 'g', label = 'background')
plt.plot(bin_edges[0:-1], vesicles, 'r', label = 'vesicles')
plt.plot(bin_edges[0:-1], axon, 'b', label = 'axon')
plt.plot(bin_edges[0:-1], PSD, 'c', label = 'PSD')
plt.plot(bin_edges[0:-1], mitochondria, 'm', label = 'mitochondria')
plt.plot(bin_edges[0:-1], mitochondrial_boundaries, 'y', label = 'mitochondrial boundaries')
plt.plot(bin_edges[0:-1], boundaries, 'k', label = 'boundaries')
plt.legend()
