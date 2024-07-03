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

# MH_03
mkdir -p MH03 && cd MH03
wget http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/machine_hall/MH_03_medium/MH_03_medium.zip
unzip MH_03_medium.zip
cd ..

# MH_04
mkdir -p MH04 && cd MH04
wget http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/machine_hall/MH_04_difficult/MH_04_difficult.zip
unzip MH_04_difficult.zip
cd ..

# MH_05
mkdir -p MH05 && cd MH05
wget http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/machine_hall/MH_05_difficult/MH_05_difficult.zip
unzip MH_05_difficult.zip
cd ..
