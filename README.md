# copopy
Code for extracting 3D coordinates from a stereocamera setup and to analyse the relative movement of copopods  

## What you need:
- Python 3.8
- Python 3.9 for copo_clicker


## Packages:
- opencv-python (4.5.1.48)
- numpy (1.22.2)
- matplotlib (3.5.1)
- glob2 (0.7)
- DateTime (4.4)

## How to use:
- extract the frames from your videos using **extractframes.py** (don't forget to change the path to your files and also output path)
- calibrate your setup with **stereocalibration.py** (you also need to change paths at the bottom)
- ...
- profit [^1]

- **keypoints.py**, **2d_coords.py** will be implemented at some point
- **scriptruntime.py** is a general code for getting the script runtime of your code printed out at the end



[^1]: not quite sure how tho
