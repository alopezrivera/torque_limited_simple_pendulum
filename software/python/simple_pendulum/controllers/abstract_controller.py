# here, the abstract controller class is defined, to which all controller
# classes have to adhere
from abc import ABC, abstractmethod


class AbstractController(ABC):
    """
    Abstract controller class. All controller should inherit from
    this abstract class.
    """
    @abstractmethod
    def get_control_output(self, meas_pos, meas_vel, meas_tau, meas_time):
        """
        The function to compute the control input for the pendulum actuator.
        Supposed to be overwritten by actual controllers. The API of this
        method should be adapted. Unused inputs/outputs can be set to None.

        Parameters
        ----------
        meas_pos : float
            the position of the pendulum [rad]
        meas_vel : float
            the velocity of the pendulum [rad/s]
        meas_tau : float
            the meastured torque of the pendulum [Nm]
        meas_time : float
            the collapsed time [s]

        Returns
        -------
        des_pos : float
            the desired position of the pendulum [rad]
        des_vel : float
            the desired velocity of the pendulum [rad/s]
        des_tau : float
            the torque supposed to be applied by the actuator [Nm]
        """

        des_pos = None
        des_vel = None
        des_tau = None
        return des_pos, des_vel, des_tau

    def init(self, x0):
        """
        Initialize the controller. May not be necessary.

        Parameters
        ----------
        x0 : array like
            the start state of the pendulum
        """
        self.x0 = x0

    def set_goal(self, x):
        """
        Set the desired state for the controller. May not be necessary.

        Parameters
        ----------
        x : array like
            the desired goal state of the controller
        """

        self.goal = x
