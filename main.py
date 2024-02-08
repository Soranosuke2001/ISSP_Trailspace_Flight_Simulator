from repo.model import JsbsimInterface

from helpers.read_config import read_setup, read_ic_aircraft

if __name__ == "__main__":
    aircraft_model, timestep, mass, throttle, wind, ini_vel, ini_alt = read_setup()
    phiItgt, thetaItgt, psiItgt, altItgt = read_ic_aircraft()

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

    # simulation
    while True:
        sim.run()

        # set the throttle
        sim.set_throttle()

        # setting aileron
        aileron = sim.calc_aileron(phiItgt)

        # continue from here
    