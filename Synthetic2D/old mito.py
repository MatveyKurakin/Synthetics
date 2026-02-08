from __future__ import print_function
import argparse
import os
import random
import torch
import numpy as np
import matplotlib.pyplot as plt
import torch.nn as nn

import cv2

# Set random seed for reproducibility
#manualSeed = 998
#manualSeed = random.randint(1, 10000) # use if you want new results
#print("Random Seed: ", manualSeed)
#random.seed(manualSeed)
#torch.manual_seed(manualSeed)

class Generator(nn.Module):
    def __init__(self, nz=100, ngf=64):
        super(Generator, self).__init__()
        self.main = nn.Sequential(
        # input is Z, going into a convolution
        nn.ConvTranspose2d( nz, ngf * 8, 4, 1, 0, bias=False),
        nn.BatchNorm2d(ngf * 8),
        nn.ReLU(True),
            # state size. (ngf*8) x 4 x 4
        nn.ConvTranspose2d(ngf * 8, ngf * 4, 4, 2, 1, bias=False),
        nn.BatchNorm2d(ngf * 4),
        nn.ReLU(True),
            # state size. (ngf*4) x 8 x 8
        nn.ConvTranspose2d( ngf * 4, ngf * 2, 4, 2, 1, bias=False),
        nn.BatchNorm2d(ngf * 2),
        nn.ReLU(True),
            # state size. (ngf*2) x 16 x 16
        nn.ConvTranspose2d( ngf * 2, ngf, 4, 2, 1, bias=False),
        nn.BatchNorm2d(ngf),
        nn.ReLU(True),
            # state size. (ngf) x 32 x 32
        nn.ConvTranspose2d( ngf, 1, 4, 2, 1, bias=False),
        nn.Tanh()
            # state size. (nc) x 64 x 64
        )

    def forward(self, input):
        return self.main(input)


class MitoGenerator():
    def __init__(self):
        # Init device
        self.device = torch.device("cuda:0" if (torch.cuda.is_available()) else "cpu")

        # Load model
        self.mitoModel = Generator()
        self.mitoModel=torch.load('mito').to(self.device)
        self.mitoModel.eval()

    def generate(self):
        # Samples num
        samples_num = 1
        noise = torch.randn(samples_num, 100, 1, 1, device=self.device)
        image = self.mitoModel(noise).detach().cpu()
        return np.squeeze(image)

generator = MitoGenerator()

for i in range(20):
    gen_image = generator.generate()
    gen_image = ((gen_image.numpy()[:,:] + 1) * 128).astype(np.uint8)

    gen_image = cv2.resize(gen_image, (128,128))

    gen_image[gen_image[:,:] < 15] = 0

    cv2.imwrite('gen'+str(i)+'.png', gen_image)


plt.figure(figsize=(20, 20))
plt.axis("off")
plt.title("Fake Images")
plt.imshow(gen_image, cmap='gray')
plt.show()
