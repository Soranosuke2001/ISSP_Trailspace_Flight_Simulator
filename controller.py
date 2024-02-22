class Controller:
    def __init__(self):
        self.throttle = 0.5  # Initial throttle setting to maintain level flight
        self.Kp_phi = 0.1  # Proportional gain for roll control
        self.Ki_phi = 0.01  # Integral gain for roll control
        self.phi_error_integral = 0.0  # Integral of phi error
        
        self.Kp_alt = 0.05  # Proportional gain for altitude control
        self.Ki_alt = 0.005  # Integral gain for altitude control
        self.alt_error_integral = 0.0  # Integral of altitude error
        
        # Assuming these are the control limits
        self.max_aileron = 1.0
        self.max_elevator = 1.0
        self.max_throttle = 1.0

    def step(self, simulation_inputs):
        # Roll control to keep wings level (phiSetpoint should be 0 for straight flight)
        phi_error = simulation_inputs['phiSetpoint'] - simulation_inputs['phi']
        self.phi_error_integral += phi_error
        aileron_command = (self.Kp_phi * phi_error + 
                           self.Ki_phi * self.phi_error_integral)
        aileron_command = max(min(aileron_command, self.max_aileron), -self.max_aileron)
        
        # Altitude control to maintain a constant altitude
        alt_error = simulation_inputs['altSetpoint'] - simulation_inputs['alt']
        self.alt_error_integral += alt_error
        elevator_command = (self.Kp_alt * alt_error + 
                            self.Ki_alt * self.alt_error_integral)
        elevator_command = max(min(elevator_command, self.max_elevator), -self.max_elevator)
        
        # Adjust throttle gradually to maintain altitude (simplified control logic)
        # In a more complex model, throttle adjustments could be more dynamic based on altitude error and rate of climb/descent
        throttle_command = self.throttle  # For simplicity, keeping throttle constant; adjust as needed

        return {
            'throttle': throttle_command,
            'aileronComm': aileron_command,
            'elevator': elevator_command,
        }
