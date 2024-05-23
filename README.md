### Note about instances :

The instances must be placed in the folder data/ in order to run the code properly. 

To build the 1.000.000 products instance, just run the large_instance_generator.py file. 


### Files description
## Description :
- AP_problem.py contains the class that regroups the different formulation of the AP problem. It must not be run.
- First_imp.py contains the code of our polynomial algorithm that solves AP. It must not be run. 
- lagrangian.py contains the binary search and the plot generator for the primal and dual bounds of the Lagrangian relaxation. Run this file to generate the plots of the primal and dual bounds for both small and medium instances. The plots are saved in png format. 
- large_instance_generator.py generates the large instances files in the data folder, i.e large-mu.csv and large-r.csv
- main.py generates the csv files that contains the min, max and average objective value and min, max and average run-time. The names of the csv are Test_instances_small, Test_instances_medium and Test_instances_large

## Can be ran :
- lagrangian.py
- large_instance_generator.py
- main.py

## Must not be ran : 
- AP_problem.py
- First_imp.py
- 