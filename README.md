# IdentiFido

##Project Summary
The goal of IdentiFido is to train a neural net on purebreed dogs. Once the neural net is trained, it will attempt to predict the composition of mixed breed dogs by similarity to purebreeds.

##Webapp - [identifido.net](http://identifido.net)
Learn more about the project there, or submit your own pictures for classification.

##Repo Structure
* app - contains all files associated with hoping the webapp
  * predict - all models/files used to predict on the webapp
  * static - static images/css
  * templates - html for webapp
* aux_files - contains all the auxiliary files that didn't fit nicely in the other folders
* model - contains the temporary and stored models as hdf5, as well as jsons of parameters and model training history
* src - master scripts for model building and evaluation/visualization
  * image_utils - collection of scripts for preprocessing/moving images around
  * old_scripts - old scripts that are no longer used
  * pymodels - python files that contain the model architectures
* todo - to do list
