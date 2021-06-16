import numpy as np

from model.params import *

class PendulumPlant(Environment, Robot, Joints, Links, Actuators):
    def __init__(self):

        """
        The PendulumPlant class contains the kinematics and dynamics
        of the simple pendulum.
        The class is initilized with the following parameters:
            - mass:         float, pendulum mass, unit: kg
            - length:       float, pendulum length, unit: m
            - damping:      float, damping factor (proportional to velocity),
                            unit: kg*m/s
            - gravity:      float, gravity (positive direction points down),
                            unit: m/s^2
            - coulomb_fric: float, friction term, (independent of magnitude
                            of velocity), unit: Nm
            - inertia:      float, inertia of the pendulum
                            (defaults to point mass inertia)
                            unit: kg*m^2
            - torque_limit: float, maximum torque that the motor can apply
                            unit: Nm

        The state of the pendulum in this class is described by
            state = [angle, angular velocity]
            (array like with len(state)=2)
            in units: rad and rad/s
        The zero state of the angle corresponds to the pendulum hanging down.
        The plant expects an actuation input (tau) either as float or array like
        (in which case the first entry is used (which should be a float))
        """

        self.m = link_01.mass                   # Overall mass
        self.m_p = link_01.mass_p               # Point mass at link end
        self.m_l = link_01.mass_l               # Link mass without point mass
        self.l = link_01.length    
        self.b = joint_01.b                     # damping
        self.g = earth.gravity
        self.coulomb_fric = joint_01.fc
        self.inertia = ((self.m_l*self.l**2)/3 + self.m_p*self.l**2)
        self.torque_limit = ak80_6_01.tau_max

        self.dof = sp.dof
        self.n_actuators = sp.n_actuators
        self.base = sp.origin
        self.n_links = sp.n_links
        self.workspace_range = [[-1.2*self.l, 1.2*self.l],
                                [-1.2*self.l, 1.2*self.l]]

    def forward_kinematics(self, pos):

        """
        Computes the forward kinematics.
        input:
            - pos:  float, angle of the pendulum
        returns:
            - A list containing one list (for one end-effector)
              The inner list contains the x and y coordinates
              for the end-effector of the pendulum
        """

        ee_pos_x = self.l * np.sin(pos)
        ee_pos_y = -self.l*np.cos(pos)
        return [[ee_pos_x, ee_pos_y]]

    def inverse_kinematics(self, ee_pos):

        """
        Comutes inverse kinematics
        input:
            - ee_pos: array like, len(state)=2
                      contains the x and y position of the end_effector
                      floats, units: m
        returns:
            - float, angle of the pendulum, unit: rad
        """

        pos = np.arctan2(ee_pos[1], ee_pos[0])
        return pos

    def forward_dynamics(self, state, tau):

        """
        Computes forward dynamics
        input:
            - state: array like, len(state)=2
                     The state of the pendulum [angle, angular velocity]
                     floats, units: rad, rad/s
            - tau: float, motor torque, unit: Nm
        returns:
            - float, angular acceleration, unit: rad/s^2
        """

        torque = np.clip(tau, -np.asarray(self.torque_limit),
                         np.asarray(self.torque_limit))

        accn = (torque - self.m * self.g * self.l * np.sin(state[0]) -
                self.b * state[1] -
                np.sign(state[1])*self.coulomb_fric) / self.inertia
        return accn

    def rhs(self, t, state, tau):

        """
        Computes the integrand of the equations of motion.
        input:
            - t:        float, time, not used
            - state:    array like, len(state)=2
                        The state of the pendulum [angle, angular velocity]
                        floats, units: rad, rad/s
            - tau: float or array like, motor torque, unit: Nm
        returns:
            - integrand, i.e.
              [angular velocity, angular acceleration]
        """

        if isinstance(tau, (list, tuple, np.ndarray)):
            torque = tau[0]
        else:
            torque = tau

        accn = self.forward_dynamics(state, torque)

        res = np.zeros(2*self.dof)
        res[0] = state[1]
        res[1] = accn
        return res