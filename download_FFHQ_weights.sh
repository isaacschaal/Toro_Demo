#!/bin/bash

# Use this script to download the pretrained FFHQ StyleGAN
# weights, provided by Nvidia at https://github.com/NVlabs/stylegan
# If you are using a custom trained model, this script can be ignored.

# This code was adapted from https://stackoverflow.com/questions/25010369/wget-curl-large-file-from-google-drive

# The name and ID of the FFHQ weights
fileid="1MEGjdvVpUsu1jB4zrXZN7Y4kBBOzizDQ"
filename="karras2019stylegan-ffhq-1024x1024.pkl"
curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=${fileid}" -o "${filename}"

# clean up the cookies
rm cookie
