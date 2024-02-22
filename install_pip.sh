#!/usr/bin/env bash
# install pytorch
pip install torch==1.13.0 torchvision==0.14.0 --index-url https://download.pytorch.org/whl/cu117
# torch-scatter
pip install torch-scatter -f https://data.pyg.org/whl/torch-1.13.0+cu117.html
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