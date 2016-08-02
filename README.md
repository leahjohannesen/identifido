# IdentiFido

##Project Summary
The goal of IdentiFido is to train a neural net on purebreed dogs. Once the neural net is trained, it will attempt to predict the composition of mixed breed dogs by similarity to purebreeds.

##Repo Structure
* app - contains all files associated with hoping the webapp
* aux_files - contains all the auxiliary files such as breed/image lists
* model - contains the stored models as hdf5, as well as jsons of parameters and model training history
* src - master scripts for model building and test
  * image_utils - collection of scripts for preprocessing/moving images around
  * old_scripts - old scripts that are no longer used
  * pymodels - all model python files
* todo - to do list
