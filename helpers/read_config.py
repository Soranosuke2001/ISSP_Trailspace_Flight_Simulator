import json
from constants.constants import filename

def read_config():
    with open(filename, 'r') as file:
        data = json.load(file)

    return data


def read_ic_aircraft():
    data = read_config()

    phiItgt = data['ic_aircraft']['phiItgt']
    thetaItgt = data['ic_aircraft']['thetaItgt']
    psiItgt = data['ic_aircraft']['psiItgt']
    altItgt = data['ic_aircraft']['altItgt']

    return phiItgt, thetaItgt, psiItgt, altItgt


def read_file_config():
    data = read_config()

    csv_filename = data['file']['csv_filename']
    decimals = data['file']['decimals']

    return csv_filename, decimals


def read_setup():
    data = read_config()

    aircraft_model = data['setup']['aircraft_model']
    timestep = data['setup']['timestep']
    mass = data['setup']['mass']
    throttle = data['setup']['throttle']
    wind = data['setup']['wind']
    ini_velocity = data['setup']['ini_velocity']
    ini_altitude = data['setup']['ini_altitude']

    return aircraft_model, timestep, mass, throttle, wind, ini_velocity, ini_altitude

def read_wind_config():
    data = read_config()
    wind_config = data.get('wind', {})
    print("Wind Config:", wind_config)  # Debug print

    return wind_config
