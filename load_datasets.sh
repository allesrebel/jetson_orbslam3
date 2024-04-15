#!/bin/bash

mkdir -p Datasets && cd Datasets && mkdir -p EuRoc && cd EuRoc

# MH_01
mkdir -p MH01 && cd MH01
wget http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/machine_hall/MH_01_easy/MH_01_easy.zip
unzip MH_01_easy.zip
cd ..

# MH_02
mkdir -p MH02 && cd MH02
wget http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/machine_hall/MH_02_easy/MH_02_easy.zip
unzip MH_02_easy.zip
cd ..
