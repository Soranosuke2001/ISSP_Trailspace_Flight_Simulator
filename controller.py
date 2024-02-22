class Controller:

    # parameters
    Kp_phi = 1
    Ki_phi = 0.01
    Kd_alt = 0.002
    thetaMax = 0.15
    throttleRamp = 0.001

    # ICs
    phiItgt = 0.0
    thetaItgt = 0.0
    psiItgt = 0
    altItgt = 0
    
    # outputs
    throttle = 0
    aileronComm = 0.0

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
        self.phiItgt = self.phiItgt + phiErr
        self.aileronComm = self.Kp_phi*phiErr + self.Ki_phi*self.phiItgt

        # bring other controllers here
        
        # Altitude control
        altErr = (simulation_inputs['altSetpoint'] - simulation_inputs['alt'])
        self.altItgt = self.altItgt + altErr
        pitchComm = self.Kd_alt * altErr + self.altItgt

        # Saturate pitch command within limits
        pitchComm = max(min(pitchComm, self.thetaMax), -self.thetaMax)

        # Update target pitch angle
        self.thetaItgt = pitchComm

        # Return the calculated control surface commands
        return {
            'throttle': self.throttle,
            'aileronComm': self.aileronComm,
            'pitchComm': pitchComm
        }