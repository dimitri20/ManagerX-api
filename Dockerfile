FROM python:3.12.5-slim

# 2. Set Environment Variables
# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# 3. Set Work Directory
# Create and set the working directory in the container
WORKDIR /usr/src/app

# 4. Install Dependencies
# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt to the container
COPY requirements.txt /usr/src/app/

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5. Copy Project Files
# Copy the rest of the application code to the working directory in the container
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
COPY . /usr/src/app

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]