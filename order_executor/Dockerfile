# Use an official Python runtime as the base image
FROM python:3.11

# Set the working directory in the container
# Both the utils and src folders will be mounted as volumes, please see docker-compose.yaml
WORKDIR /app

# Copy the requirements file to the working directory
COPY ./order_executor/requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable so logs show up immediately
ENV PYTHONUNBUFFERED=1

# Set the command to run the application
CMD python utils/other/hotreload.py "order_executor/src/app.py"


## Use an official Python runtime as the base image
#FROM python:3.11
#
## Set the working directory in the container
#WORKDIR /app
#
## Copy requirements file
#COPY ./order_executor/requirements.txt .
#
## Install Python dependencies
#RUN pip install --no-cache-dir -r requirements.txt
#
## Set environment variable so logs show up immediately
#ENV PYTHONUNBUFFERED=1
#
## CMD uses hotreload to run app.py from src folder
#CMD ["python", "utils/other/hotreload.py", "order_executor/src/app.py"]



