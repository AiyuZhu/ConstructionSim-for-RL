# ConstructionSim-for-RL

A simple construction simulator to set up a framework available for RL (currently only for the value-based method). 

### A simple construction simulator
Voxel-based construction simulator allows for site size adjustment and custom length adjustment of components.

### Setup environment
python 3.7
stable-baseline3
pygame
pyOpenGL

### Upload new env construction_RL
you can set up init and target position random or fixed

###Set up your components
You can create component use SCO. See SCO.py in BIM class for attr detials. 
We build the component in siteOly_multi_tar.py
For example, in siteOnly_multi_tar line 86-88, create three components.
####Set up init position for components
When train on is True, your init position is random.
####Set up target position for components.
If you want fixed target position, delete tar_list in line 31 in siteOly_multi_tar.py and the for loop in line 1569.


