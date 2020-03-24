## This script is used to create a *.for_g_all.pt file
## from a TF StyleGAN *.pkl file

## It is hard coded to convert the karras2019stylegan-ffhq-1024x1024.pkl file
## but can be modified to convert any custom TF StyleGAN *.pkl file

## This code is slightly modified from https://github.com/lernapparat/lernapparat/blob/541b6b1f21cbce602c4981cb3fb73f75b42227c8/style_gan/pytorch_style_gan.ipynb
## Comments with one "#" are from the original version, while commments
## with two "##" are provided by me

########################

## Import packages
import torch
import torch.nn as nn
import torch.nn.functional as F
import os
from collections import OrderedDict
import pickle
import numpy as np
import torchvision
from torchvision.utils import save_image
import dnnlib, dnnlib.tflib

## Import the Torch Network
from torchlib.torch_network import *

## Initialize the network
g_all = nn.Sequential(OrderedDict([
    ('g_mapping', G_mapping()),
    #('truncation', Truncation(avg_latent)),
    ('g_synthesis', G_synthesis())
]))

# this can be run to get the weights, but you need the reference implementation and weights

dnnlib.tflib.init_tf()
weights = pickle.load(open('./karras2019stylegan-ffhq-1024x1024.pkl','rb'))
weights_pt = [OrderedDict([(k, torch.from_numpy(v.value().eval())) for k,v in w.trainables.items()]) for w in weights]
torch.save(weights_pt, './karras2019stylegan-ffhq-1024x1024.pt')

# then on the PyTorch side run
state_G, state_D, state_Gs = torch.load('./karras2019stylegan-ffhq-1024x1024.pt')
def key_translate(k):
    k = k.lower().split('/')
    if k[0] == 'g_synthesis':
        if not k[1].startswith('torgb'):
            k.insert(1, 'blocks')
        k = '.'.join(k)
        k = (k.replace('const.const','const').replace('const.bias','bias').replace('const.stylemod','epi1.style_mod.lin')
              .replace('const.noise.weight','epi1.top_epi.noise.weight')
              .replace('conv.noise.weight','epi2.top_epi.noise.weight')
              .replace('conv.stylemod','epi2.style_mod.lin')
              .replace('conv0_up.noise.weight', 'epi1.top_epi.noise.weight')
              .replace('conv0_up.stylemod','epi1.style_mod.lin')
              .replace('conv1.noise.weight', 'epi2.top_epi.noise.weight')
              .replace('conv1.stylemod','epi2.style_mod.lin')
              .replace('torgb_lod0','torgb'))
    else:
        k = '.'.join(k)
    return k

def weight_translate(k, w):
    k = key_translate(k)
    if k.endswith('.weight'):
        if w.dim() == 2:
            w = w.t()
        elif w.dim() == 1:
            pass
        else:
            assert w.dim() == 4
            w = w.permute(3, 2, 0, 1)
    return w

# we delete the useless torgb filters
param_dict = {key_translate(k) : weight_translate(k, v) for k,v in state_Gs.items() if 'torgb_lod' not in key_translate(k)}
if 1:
    sd_shapes = {k : v.shape for k,v in g_all.state_dict().items()}
    param_shapes = {k : v.shape for k,v in param_dict.items() }

    for k in list(sd_shapes)+list(param_shapes):
        pds = param_shapes.get(k)
        sds = sd_shapes.get(k)
        if pds is None:
            print ("sd only", k, sds)
        elif sds is None:
            print ("pd only", k, pds)
        elif sds != pds:
            print ("mismatch!", k, pds, sds)

g_all.load_state_dict(param_dict, strict=False) # needed for the blur kernels

## Save the generator as a .pt file
torch.save(g_all.state_dict(), './karras2019stylegan-ffhq-1024x1024.for_g_all.pt')

## Delete the unnecceasry .pt file
os.remove("./karras2019stylegan-ffhq-1024x1024.pt")
