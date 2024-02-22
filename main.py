from model import JsbsimInterface
from controller import Controller
import os
from helpers.read_config import read_setup

if __name__ == "__main__":
    aircraft_model, timestep, mass, throttle, wind, ini_vel, ini_alt = read_setup()

    # set the initial conditions
    sim = JsbsimInterface(
        None,
        aircraft_model = aircraft_model,
        initial_altitude_ft = ini_alt,
        initial_velocity_kts = ini_vel,
        mass_kg = mass,
        wind = wind,
        throttle = throttle,
    )
    sim.set_dt(timestep)
    current_working_directory = os.getcwd()
    full_path = os.path.join(current_working_directory, 'config/flightgear.xml')
    sim.set_output_directive(full_path)

    # check initial conditions and print aircraft config
    sim.check_ic()
    sim.print_config()

    # initialize controller object
    controllerObj = Controller(dT = timestep)

    # simulation
    while True:

        # call the controller step function
        sim_inputs = {
            'phiSetpoint': 0.15,
            'phi': sim['attitude/roll-rad'],
            'theta': sim['attitude/pitch-rad'],
            'altSetpoint': 1000,
            'alt': sim['position/h-sl-ft']
        }
        ctrlOutput = controllerObj.step(sim_inputs)
        
        # run simulation one time step
        sim.set_throttle(ctrlOutput['throttle'])
        sim.set_control_surfaces(ctrlOutput['aileronComm'], ctrlOutput['elevatorComm'], 0.0)
        sim.run_simulation_step()

        print(sim['position/h-sl-ft'])
        # continue from here
        if sim['position/h-sl-ft'] <= 0:
            break
