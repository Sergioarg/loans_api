# Use the Python base image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file (requirements.txt)
COPY requirements.txt .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project source code to /app
COPY . .

# Expose port 8000 (Django's default port)
EXPOSE 8000

# Command to run Django's development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
