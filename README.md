# Dynamic Origin-Distination Demand Calibration for Network Traffic Congestion Reconstruction
Ying-Chuan Ni <br />
Traffic Engineering Group, Institute for Transport Planning and Systems, ETH Zurich

## Introduction
Existing traffic demand estimation/validation work often neglects the replication of link-level traffic states. This repository showcases the method to calibrate dynamic origin-destination demand that is able to reconstruct the traffic congestion pattern in an urban road network. For more information, the users are referred to the research article.

## SUMO ground-truth scenarios
An uncongested scenario and a congested scenario are designed for a modified Sioux-Falls network, as shown in the image below. The SUMO simulation packages can be found in the folder SUMO_scenario_uncon and SUMO_scenario_con.
EdgeOutput files are required for the demand calibration.

<img width="225" height="295" alt="Link_speed_5400" src="https://github.com/user-attachments/assets/21d1609b-0446-44e2-8a86-d52b20ccf376" />

The scenario_analysis.py file prepares all the information required for the mathematical optimization.

## Mathematical optimization
The calculation_functions.py contains the route (OD-to-link) travel time calculation functions. In grb_problem.py, the mathematical optimization problem is implemented using the gurobipy library. The main.py file executes the code and saves the variables in a .pickle file.

## Reproduced SUMO simulation
The update_OD.py file can be used to read in the saved variables and change the demand in the .xml file for SUMO simulation.

## To cite
Coming soon

## Contact information
For questions, please feel free to contact the author via email (ying-chuan.ni@ivt.baug.ethz.ch).
