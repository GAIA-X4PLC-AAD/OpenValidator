# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
# COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir scipy lxml

# Copy the entire codebase to the working directory
COPY . .

RUN ["chmod", "+x", "entrypoint.sh"]

RUN ["chmod", "+x", "entrypoint_GitHubAction_Open_Validator.sh"]

# Set the entry point for the container
# CMD [ "python3", "main.py" ]

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint_GitHubAction_Open_Validator.sh"]