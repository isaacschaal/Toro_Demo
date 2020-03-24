## This script is used to generate new samples from a StyleGAN network
## from a *.for_g_all.pt file

## It is hard coded to use the karras2019stylegan-ffhq-1024x1024.for_g_all.pt file
## but can be modified to use any custom *.for_g_all.pt file

# It recieves the week as input, and uses that to save the
# images in the correct folder

## This code is modified from https://github.com/lernapparat/lernapparat/blob/541b6b1f21cbce602c4981cb3fb73f75b42227c8/style_gan/pytorch_style_gan.ipynb
## Comments with one "#" are from the original version, while commments
## with two "##" are provided by me

########################

## Add the Toro_Demo folder to the sys path
## so that the script can import dnnlib and torchlib
import sys
sys.path.insert(0,'.')

## Import packages
import torch
import torch.nn as nn
import torch.nn.functional as F
import os
from collections import OrderedDict
import pickle
import argparse
import numpy as np
import torchvision
from torchvision.utils import save_image
import dnnlib, dnnlib.tflib

## Import the Torch Network
from torchlib.torch_network import *

## Parse Args
parser = argparse.ArgumentParser()
parser.add_argument("--week", type=str, help="The number of the week")

def main(week):

    ## Initialize the newtork
    g_all = nn.Sequential(OrderedDict([
        ('g_mapping', G_mapping()),
        #('truncation', Truncation(avg_latent)),
        ('g_synthesis', G_synthesis())
    ]))

    ## Load the weights
    g_all.load_state_dict(torch.load('./karras2019stylegan-ffhq-1024x1024.for_g_all.pt'))

    ## GENERATING IMAGES
    device = 'cpu'
    g_all.eval()
    g_all.to(device)

    ## set the seed as the week
    torch.manual_seed(week)
    nb_samples = 5

    ## Generate latent vectors
    latents = torch.randn(nb_samples, 512, device=device)

    ## Sample
    with torch.no_grad():
        imgs = g_all(latents)
        imgs = (imgs.clamp(-1, 1) + 1) / 2.0 # normalization to 0..1 range
    imgs = imgs.cpu()

    ## make a directory
    dir = './img_folders/week_' + str(week)
    if not os.path.exists(dir):
        os.mkdir(dir)

    ## Save samples
    for i in range(nb_samples):
        save_image(imgs[i], dir+"/img"+str(i)+".png")

if __name__ == '__main__':
    args = parser.parse_args()
    week = args.week
    main(week)
