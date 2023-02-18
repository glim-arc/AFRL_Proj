# hw4_pid_tuning

You will be manually tuning the altitude controller for the crazyflie.

## Instructions

* Read the crazyflie documentation to find what gains to change to modify the altitude PID gains and how to obtain the altitude of the vehicle and motor commands for logging.
* Plot the altitude and sum of motor inputs for your crazyflie taking off with original mass.
* Plot the altitude and sum of motor inputs for your crazyflie taking off with a penny, or similar small weight taped to the bottom of the vehicle.
* Tune your altitude PID controller and report the original and updated gains for the added weight.

## Deliverables

* Plot for altitude and sum of motor inputs response for original and new mass during takeoff.
* Written comparison of the original and new gains and an explanation of your tuning process. How is the trim thrust of the crazyflie computed for hover? Investigate the c code of the PID controller and explain the implementation of the altitude PID controller. Is there a wind-up guard? Is there saturation? Is there a trim mass of the vehicle?
* Video of your original takeoff with the weight, and your tuned take-off with the weight.
