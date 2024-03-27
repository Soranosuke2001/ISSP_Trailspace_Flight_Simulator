import jsbsim
import pandas as pd
from math import radians, cos, sin
from constants.constants import *
from helpers.read_config import read_file_config

class JsbsimInterface(jsbsim.FGFDMExec):
    def __init__(self, pm_root, aircraft_model='Rascal110-JSBSim', initial_altitude_ft=1000, initial_velocity_kts=100, mass_kg=1000, wind=100, throttle=0):
        # self.exec = jsbsim.FGFDMExec(None)
        super().__init__()
        self.set_debug_level(0)
        self.load_model(aircraft_model)

        csv_filename, decimals = read_file_config()
        self.csv_filename = csv_filename
        self.decimals = decimals
        
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

    def update_simulation_data(self, data):
        data['altitude'].append(round(self['position/h-sl-ft'], self.decimals))

        data['xaccel'].append(round(self.get_property_value('accelerations/udot-ft_sec2'), self.decimals))
        data['yaccel'].append(round(self.get_property_value('accelerations/vdot-ft_sec2'), self.decimals))
        data['zaccel'].append(round(self.get_property_value('accelerations/wdot-ft_sec2'), self.decimals))
        
        data['elevator'].append(round(self.get_property_value('fcs/elevator-cmd-norm'), self.decimals))
        data['aileron'].append(round(self.get_property_value('fcs/aileron-cmd-norm'), self.decimals))
        data['rudder'].append(round(self.get_property_value('fcs/rudder-cmd-norm'), self.decimals))
    
    def save_simulation_data(self, data):
        df = pd.DataFrame(data)
        df.to_csv(self.csv_filename, index=False)

    def set_wind(self, wind_config):
        direction_deg = wind_config.get('direction_deg', 0)
        speed_kts = (wind_config.get('speed_kts_min', 0) + wind_config.get('speed_kts_max', 0)) / 2
        
        # Convert wind speed from knots to feet per second (1 kt = 1.68781 ft/s)
        speed_fps = speed_kts * 1.68781
        
        # Calculate NED components based on wind direction and speed
        wind_north = speed_fps * cos(radians(direction_deg))
        wind_east = speed_fps * sin(radians(direction_deg))
        wind_down = -10  # Assuming no vertical wind component
        
        # Set wind using the NED properties
        self['atmosphere/wind-north-fps'] = wind_north
        self['atmosphere/wind-east-fps'] = wind_east
        self['atmosphere/wind-down-fps'] = wind_down