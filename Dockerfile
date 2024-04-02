# Base image for the simulation environment
FROM python:3.11.7

# Install dependencies for creating virtualenv
RUN apt-get update
RUN apt-get install -y python3-venv

RUN pip install --no-cache-dir awscli

# Create a working directory
WORKDIR /app

COPY . .

# Create a virtual environment
RUN python3 -m venv venv

# Activate the virtual environment (source command for bash-based shells)
ENV PATH="/app/venv/bin:$PATH"

# Copy requirements.txt
COPY requirements.txt .

# Install python dependencies using pip within the virtual environment
RUN pip install -r requirements.txt

COPY Rascal110-JSBSim /app/venv/lib/python3.11/site-packages/jsbsim/aircraft/Rascal110-JSBSim

# Command to run the python script
CMD [ "python", "app.py" ]
