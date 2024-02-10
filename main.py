from repo.model import JsbsimInterface
from controller import Controller

from helpers.read_config import read_setup, read_ic_aircraft

if __name__ == "__main__":
    aircraft_model, timestep, mass, throttle, wind, ini_vel, ini_alt = read_setup()

    # set the initial conditions
    sim = JsbsimInterface(
        aircraft_model,
        ini_alt,
        ini_vel,
        mass,
        wind,
        throttle,
    )
    sim.set_dt(timestep)

    # check initial conditions and print aircraft config
    sim.check_ic()
    sim.print_config()

    # initialize controller object
    controllerObj = Controller()

    # simulation
    while True:

        # call the controller step function
        sim_inputs = {
            'phiSetpoint': 0.15,
            'phi': sim.exec['attitude/roll-rad'],
        }
        ctrlOutput = controllerObj.step(sim_inputs)

        # run simulation one time step
        sim.set_throttle(ctrlOutput['throttle'])
        sim.set_control_surfaces(ctrlOutput['aileronComm'], 0.0, 0.0)
        sim.run()

        # continue from here
