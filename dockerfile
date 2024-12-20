# Step 1: Use an official Python runtime as a parent image
FROM python:3.9

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Copy the current directory contents into the container
COPY . /app

# Step 4: Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Make port 5000 available to the world outside the container
EXPOSE 5000

# Step 6: Define environment variable
ENV FLASK_APP=app.py

# Step 7: Run the app
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]
