FROM python:3.10

# Set the working directory to /app.
# A working directory helps organize the structure 
# of the project being built to an image
WORKDIR /app

# Copy the requirements.txt file from the local directory 
# to the working directory on the Docker container
COPY requirements.txt /app/requirements.txt

# Uprade pip and install requirements
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Exposes the PORT from which our application 
# can be accessed from the local network
EXPOSE 8080

# Copy the rest of the files and folders 
# into the Docker container working directory
COPY ./ /app

# Start the application
CMD ["python", "main.py"]