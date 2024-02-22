import jsbsim

from constants.constants import *

class JsbsimInterface(jsbsim.FGFDMExec):
    def __init__(self, pm_root, aircraft_model='Rascal110-JSBSim', initial_altitude_ft=1000, initial_velocity_kts=100, mass_kg=1000, wind=100, throttle=0):
        # self.exec = jsbsim.FGFDMExec(None)
        super().__init__()
        self.set_debug_level(0)
        self.load_model(aircraft_model)
        
        # Set initial conditions
        self['ic/h-sl-ft'] = initial_altitude_ft  # Initial altitude in feet
        self['ic/vc-kts'] = initial_velocity_kts  # Initial airspeed in knots
        self['propulsion/engine/set-running'] = 1 # Start with engine running
        self['mass-properties/mass[0]'] = mass_kg # Set the mass of the aircraft
        self['fcs/throttle-cmd-norm'] = throttle  # Set the throttle of the aircraft

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

    def set_throttle(self, throttle =0.0):
        self['fcs/throttle-cmd-norm'] = throttle
    
    def set_control_surfaces(self, aileron=0.0, elevator=0.0, rudder=0.0):
        """Adjust control surfaces. Values range from -1.0 to 1.0."""
        self['fcs/aileron-cmd-norm'] = aileron    # Aileron control
        self['fcs/elevator-cmd-norm'] = elevator  # Elevator control
        self['fcs/rudder-cmd-norm'] = rudder      # Rudder control

    def adjust_velocity_and_altitude(self, velocity_kts=None, altitude_ft=None):
        """Adjust the aircraft's velocity and altitude."""
        if velocity_kts is not None:
            self['ic/vc-kts'] = velocity_kts
        if altitude_ft is not None:
            self['ic/h-sl-ft'] = altitude_ft

    def run_simulation_step(self, delta_time=1.0):
        """Advance the simulation by a specified time step in seconds."""
        self.run()     # Advance the simulation

    def get_simulation_data(self):
        """Retrieve relevant simulation data."""
        return {
            'altitude': self['position/h-sl-ft'],
            'velocity': self['velocities/vc-kts'],
            'mass': self['mass-properties/mass[0]']
        }
