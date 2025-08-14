#!/bin/bash

python3 -m venv $HOME/venv/dicom-tools
# source ${HOME}/venv/dicom-tools/bin/activate
export PATH=$HOME/venv/dicom-tools/bin:${PATH}

pip3 install SimpleITK
pip3 install matplotlib
pip3 install numpy
pip3 install scipy
pip3 install pydicom pynetdicom

