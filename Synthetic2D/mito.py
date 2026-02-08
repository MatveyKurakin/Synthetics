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

    def make_mask(self, image):
        mask = image.copy()
        mask[mask > -0.95] = 255

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        return opening

    def generate(self):
        # Samples num
        samples_num = 1
        noise = torch.randn(samples_num, 100, 1, 1, device=self.device)
        image = self.mitoModel(noise).detach().cpu().numpy()
        image = np.squeeze(image)
        mask = self.make_mask(image)

        image = (image * 128.0 + 128.0).astype(np.uint8)

        return image, mask


generator = MitoGenerator()
image, mask = generator.generate()

for i in range(20):
    gen_image, mask = generator.generate()

    gen_image = cv2.resize(gen_image, (128,128))
    mask = cv2.resize(mask, (128,128))

    #gen_image[gen_image[:,:] < 15] = 0

    cv2.imwrite('gen'+str(i)+'.png', gen_image)
    cv2.imwrite('mask'+str(i)+'.png', mask)


fig=plt.figure(figsize=(15, 10))
plt.axis("off")
plt.title("Fake Images")
fig.add_subplot(1,2,1)
plt.imshow(image, cmap='gray')
fig.add_subplot(1,2,2)
plt.imshow(mask, cmap='gray')
plt.show()
