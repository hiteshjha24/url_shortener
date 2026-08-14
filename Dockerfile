# Step 1: Use an official lightweight Python base image
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Step 4: Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy application source code
COPY . .

# Step 6: Expose FastAPI's default port
EXPOSE 8000

# Step 7: Run the application with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]