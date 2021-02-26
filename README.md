# mibig_classifications
Retrieve chemical classes (ClassyFire/NPClassifier), as well as BGC classifications for MiBIG BGCs and their products.
These two types of classifications are then connected to eachother to form linking rules, ideally linking certain chemical and BGC classes together.

This repo is inspired by https://github.com/OscarHoekstra/ClassifyNPDB

To run the analysis from this repo, you will need to download a version of MiBIG (json format), like: https://dl.secondarymetabolites.org/mibig/mibig_json_2.0.tar.gz


## Environment
Set up an environment to be able to run the code in this repo:
```
conda create -n myenv python=3.7.2 requests rdkit
conda activate myenv
pip install jupyter
```
