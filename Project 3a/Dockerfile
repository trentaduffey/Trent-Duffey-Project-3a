# use an official python image as the base image.
FROM python:3.8-slim-buster

# set the working directory to /app
WORKDIR /app

# Copy the contents of the current directory in the container /app directory
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install any packages
RUN pip install --no-cache-dir -r requirements.txt

# Set the default commands for starting the container
CMD ["python", "script.py"]


