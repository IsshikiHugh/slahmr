#!/usr/bin/env bash
# install pytorch
pip install torch==1.13.0 torchvision==0.14.0 --index-url https://download.pytorch.org/whl/cu117
# pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --index-url https://download.pytorch.org/whl/cu118
# torch-scatter
pip install torch-scatter -f https://data.pyg.org/whl/torch-1.13.0+cu117.html
# pip install torch-scatter -f https://data.pyg.org/whl/torch-2.0.1+cu118.html
# install PHALP
pip install phalp[all]@git+https://github.com/brjathu/PHALP.git
# install source
pip install -e .
# install remaining requirements
pip install -r requirements.txt
# install ViTPose
pip install -v -e third-party/ViTPose
# install DROID-SLAM
cd third-party/DROID-SLAM
python setup.py install
cd ../..