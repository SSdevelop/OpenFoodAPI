# Using an officilal python runtime as parent image
FROM python:slim

ADD . /app

# setting the working directory    
WORKDIR /app   

# setting the env variables for our flask app
ENV FLASK_APP=app.py     
ENV FLASK_RUN_HOST=0.0.0.0

# copying the requirements file to the image file system
COPY requirements.txt requirements.txt 

# installing the dependencies of our app  
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt && pip3 install --no-cache-dir Flask flask_prometheus_metrics

# exposing the port of 15000     
EXPOSE 15000

# making our image filesystem similar to our host
COPY . .

# launching our application                                
CMD ["python3", "app.py"]   