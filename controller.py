class Controller:

    # parameters
    Kp_phi = 1
    Ki_phi = 1
    Kp_theta = 1
    Ki_theta = 1
    thetaMax = 0.15
    throttleRamp = 0.001

    # ICs
    phiItgt = 0.0
    thetaItgt = 0.0
    psiItgt = 0
    altItgt = 0
    throttle = 0

    def __init__(self, **kwargs):

        # Store other controller parameters from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def step(self, simulation_inputs):
        """
        Processes simulation inputs and calculates control actions.

        Args:
            simulation_inputs: A dictionary or other data structure containing 
                               inputs from the simulation environment.

        Returns:
            A dictionary or other data structure containing the calculated 
            control actions to be sent back to the simulator.
        """

        # slowly increase throttle and saturate it at 1.0
        self.throttle = self.throttle + self.throttleRamp
        if (self.throttle > 1):
            self.throttle = 1

        # Roll angle control
        phiErr = (simulation_inputs['phiSetpoint'] - simulation_inputs['phi'])
        self.phiItgt = self.phiItgt + phiErr*self.dT
        aileronComm = self.Kp_phi*phiErr + self.Ki_phi*self.phiItgt

        # Pitch angle control
        thetaErr = 0 - simulation_inputs['theta']
        self.thetaItgt = self.thetaItgt + thetaErr*self.dT
        elevatorComm = - (self.Kp_theta * thetaErr + self.Ki_theta*self.thetaItgt)

        # Saturate elevator and aileron command within limits
        aileronComm = max(min(aileronComm, 1.0), -1.0)
        elevatorComm = max(min(elevatorComm, 1.0), -1.0)

        # Return the calculated control surface commands
        return {
            'throttle': self.throttle,
            'aileronComm': aileronComm,
            'elevatorComm': elevatorComm
        }