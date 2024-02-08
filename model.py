import jsbsim

from constants.constants import *

class JsbsimInterface:
    def __init__(self, aircraft_model='Rascal110-JSBSim', initial_altitude_ft=1000, initial_velocity_kts=100, mass_kg=1000, wind=100, throttle=0):
        self.exec = jsbsim.FGFDMExec(None)
        self.exec.set_debug_level(0)
        self.exec.load_model(aircraft_model)
        
        # Set initial conditions
        self.exec['ic/h-sl-ft'] = initial_altitude_ft  # Initial altitude in feet
        self.exec['ic/vc-kts'] = initial_velocity_kts  # Initial airspeed in knots
        self.exec['propulsion/engine/set-running'] = 1 # Start with engine running
        self.exec['mass-properties/mass[0]'] = mass_kg # Set the mass of the aircraft
        self.exec['fcs/throttle-cmd-norm'] = throttle  # Set the throttle of the aircraft

        self.throttle = throttle

    def check_ic(self):
        success = self.run_ic()

        if not success:
            raise RuntimeError("Initial Simulation Conditions Error")
        else:
            print("Initial Simulation Conditions Met")

    def print_config(self):
        print("Simulation Config")
        print("-"*50)
        self.print_simulation_configuration()
        print()

        print("Frame Duration")
        print("-"*50)
        print(self.get_delta_t())
        print()

        # Not sure if this works
        print("Flight Simulation Object")
        print("-"*50)
        print(self)
        print()

    def set_throttle(self):
        self.exec['fcs/throttle-cmd-norm'] = self.throttle
        self.throttle = self.throttle + 0.001 * 1

        if self.throttle > 1:
            self.throttle = 1

    def calc_aileron(self, phiItgt):
        phi = self.exec['attitude/roll-rad']
        phiComm = -1 * (phi - PHI_SET_POINT)
        phiItgt = phiItgt + 0.01 * phiComm
    
    def set_control_surfaces(self, elevator=0.0, aileron=0.0, rudder=0.0):
        """Adjust control surfaces. Values range from -1.0 to 1.0."""
        self.exec['fcs/elevator-cmd-norm'] = elevator  # Elevator control
        self.exec['fcs/aileron-cmd-norm'] = aileron    # Aileron control
        self.exec['fcs/rudder-cmd-norm'] = rudder      # Rudder control

    def adjust_velocity_and_altitude(self, velocity_kts=None, altitude_ft=None):
        """Adjust the aircraft's velocity and altitude."""
        if velocity_kts is not None:
            self.exec['ic/vc-kts'] = velocity_kts
        if altitude_ft is not None:
            self.exec['ic/h-sl-ft'] = altitude_ft

    def run_simulation_step(self, delta_time=1.0):
        """Advance the simulation by a specified time step in seconds."""
        self.exec.run_ic()  # Initialize conditions
        self.exec.run()     # Advance the simulation

    def get_simulation_data(self):
        """Retrieve relevant simulation data."""
        return {
            'altitude': self.exec['position/h-sl-ft'],
            'velocity': self.exec['velocities/vc-kts'],
            'mass': self.exec['mass-properties/mass[0]']
        }
