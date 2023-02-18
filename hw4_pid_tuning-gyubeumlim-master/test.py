"""
This script shows a simple scripted flight path using the MotionCommander class.

Simple example that connects to the crazyflie at `URI` and runs a
sequence. Change the URI variable to your Crazyflie configuration.
"""
import logging
import sys
import time
import numpy as np

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.crazyflie.log import LogConfig
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils.multiranger import Multiranger

URI = 'radio://0/80/250K/E7E7E7E736'

if len(sys.argv) > 1:
    URI = sys.argv[1]

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


def is_close(range):
    MIN_DISTANCE = 0.1  # m

    if range is None:
        return False
    else:
        return range < MIN_DISTANCE


if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
    data = []


    cf = Crazyflie(rw_cache='./cache')
    with SyncCrazyflie(URI, cf = cf) as scf:
        print('Checking state.')
        log_config = LogConfig(name='Altitude test', period_in_ms=100)
        log_config.add_variable('stateEstimate.z', 'float')
        log_config.add_variable('motor.m1', 'float')
        log_config.add_variable('motor.m2', 'float')
        log_config.add_variable('motor.m3', 'float')
        log_config.add_variable('motor.m4', 'float')
        print('Log configured.')

        # set pid gains, tune down Kp to deal with UWB noise
        print(cf.param.get_value('posCtlPid.thrustBase'))
        print(cf.param.get_value('posCtlPid.zKp'))
        print(cf.param.get_value('posCtlPid.zKi'))
        print(cf.param.get_value('posCtlPid.zKd'))

        cf.param.set_value('posCtlPid.thrustBase', '36000')
        cf.param.set_value('posCtlPid.zKp', '2.2')
        cf.param.set_value('posCtlPid.zKi', '0.5')
        cf.param.set_value('posCtlPid.zKd', '0')
        print('Controller configured.')

        with SyncLogger(scf, log_config) as logger:
            with MotionCommander(scf) as mc:
                with Multiranger(scf) as multi_ranger:
                    count = 0
                    for log_entry in logger:
                        t = log_entry[0]
                        log_data = log_entry[1]
                        m1 = log_data['motor.m1']
                        m2 = log_data['motor.m2']
                        m3 = log_data['motor.m3']
                        m4 = log_data['motor.m4']
                        z = log_data['stateEstimate.z']
                        data.append([t, m1,m2,m3,m4,z])
                        count += 1
                        if count > 50:
                            break
                    

        data = np.array(data)
        np.savetxt('data.txt', data)
        print('Demo terminated!')