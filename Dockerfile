# Use the official Python image from the Docker Hub
FROM python:3.9

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libhdf5-dev \
    libhdf5-serial-dev \
    hdf5-tools \
    zlib1g-dev \
    libjpeg-dev \
    liblapack-dev \
    libblas-dev \
    gfortran \
    libatlas-base-dev \
    libboost-all-dev

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file into the container at /code/requirements.txt
COPY ./requirements.txt /code/requirements.txt

# Install the dependencies listed in the requirements file
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application code into the container at /code/Backend
COPY ./Backend /code/Backend

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/code/Backend/src

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]