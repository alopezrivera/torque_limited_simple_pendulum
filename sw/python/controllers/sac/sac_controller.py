# Other imports
from stable_baselines import SAC
import numpy as np
import yaml
import os
from pathlib import Path

# Set path for local imports
import site
site.addsitedir('../..')

# Local imports
from controllers.abstract_controller import AbstractClosedLoopController

# default parameters, can be changed
model_path = os.path.join(Path(__file__).parents[4], 'data/models/sac_model.zip')
# params_path = os.path.join(Path(__file__).parents[4],
#                            'data/parameters/sp_parameters_sac.yaml')


class SacController(AbstractClosedLoopController):
    def __init__(self, params):

        self.model = SAC.load(model_path)
        self.params = params

    def get_control_output(self, meas_pos, meas_vel, meas_tau, meas_time=0):
        if self.params['use_symmetry']:
            # map meas pos to [-np.pi, np.pi]
            meas_pos_mod = np.mod(meas_pos + np.pi, 2 * np.pi) - np.pi
            observation = np.squeeze(np.array([meas_pos_mod, meas_vel]))
            observation[0] *= np.sign(meas_pos_mod)
            observation[1] *= np.sign(meas_pos_mod)
            des_tau, _states = self.model.predict(observation)
            des_tau *= np.sign(meas_pos_mod)
        else:
            observation = np.squeeze(np.array([meas_pos, meas_vel]))
            des_tau, _states = self.model.predict(observation)
        des_tau *= float(self.params['torque_limit'])
        
        # since this is a pure torque controller, set pos_des and vel_des to None
        des_pos = None
        des_vel = None
        
        return des_pos, des_vel, des_tau

#    def return_all(self):
#        return SacController()
