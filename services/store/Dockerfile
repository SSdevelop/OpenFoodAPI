# Using an officilal python runtime as parent image
FROM python:slim

# Setting the working directory to /app
WORKDIR /app

# Copying the contents of current folder to /app
COPY . /app

# Installing the required packages from requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Running the python script when the container launches
CMD ["python", "app.py"]