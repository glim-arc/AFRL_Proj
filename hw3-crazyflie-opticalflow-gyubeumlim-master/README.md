##

I made a small box as my room is small and there is a lot of obstacles around.





# hw3-crazyflie-opticalflow
Modify the script to fly the crazyflie in a square pattern using the optical flow sensor and pausing for obstacles in its path.

## Submission

* Video of your vehicle flying the pattern and pausing if an object is inserted in its path, mp4 format, less than 5 mb. Add this as a file to your github repository for the assignment.
* Your modified script.py in this repository.

## Setup
Create an anaconda environment for the class

1. Download anaconda
1. Setup environment

```bash
conda create --name aae490iar
conda activate aae490idar
conda config --add channels conda-forge
conda config --set channel_priority strict
conda install python pyqt
pip install cfclient
```
1. Set udev permissions: https://github.com/bitcraze/crazyflie-lib-python#setting-udev-permissions

1. Reboot computer

1. Veryify connection with cfclient. Your drone should be communicate on channel 'E7E7E7E7##', where ## is your box number (01-20)

```bash
conda activate aae490iar
cfclient
```

  * Plug in the radio fully, (no leds will be on, this is ok)
  * Select scan, then connect
  * If you have an problems go here: https://www.bitcraze.io/getting-started-with-the-crazyflie-2-0/
  
1. Modify the channel in the script.py to match your box number. It should max the address in cfclient without the 0x at the beginning, and verify that the script works. It should let you push the drone around with the obstacle avoidance sensors. Waving your hand above the drone will make it land.
  
1. Modify the script to fly in a box pattern, see the motion commander example: https://github.com/bitcraze/crazyflie-lib-python/blob/master/examples/motion_commander_demo.py
