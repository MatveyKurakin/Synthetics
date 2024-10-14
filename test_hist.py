from settings import *

import matplotlib.pyplot as plt 



nums = []    
for i in range(100000): 
    nums.append(normal_randint(172,37)) 
    
for i in range(55000): 
    nums.append(normal_randint(135,55))
    
for i in range(15000): 
    nums.append(normal_randint(148,20)) 
    
    
        
# plotting a graph 
plt.xlim([0.0, 255.0])
plt.ylim([0.0, 0.10])
plt.hist(nums, bins = 256, density = True) 
plt.show()