# mibig_classifications
Retrieve chemical classes (ClassyFire/NPClassifier), as well as BGC classifications for MIBiG BGCs and their products.
These two types of classifications are then connected to eachother by counting their interactions, ideally matching certain chemical and BGC classes. Based on the relative counts of each matched pair of class-terms it is assessed how well the pair of class-terms match to eachother.

This repo is inspired by https://github.com/OscarHoekstra/ClassifyNPDB

To run the analysis from this repo, you will need to download a version of MIBiG (json format), like: https://dl.secondarymetabolites.org/mibig/mibig_json_2.0.tar.gz


## Environment
Set up an environment to be able to run the code in this repo:
```
conda create -n myenv python=3.7.2 rdkit
conda install -c plotly plotly=4.14.3
conda install -c plotly plotly-orca==1.3.1 psutil
conda activate myenv
pip install jupyter
```
