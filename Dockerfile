# Use a prebuilt Python + GDAL image
FROM andrejreznik/python-gdal:py3.11.10-gdal3.6.2

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Set working directory
WORKDIR /app

# Install system packages (for psycopg2 or other deps)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port (Gunicorn)
EXPOSE 8000

# Default command: start Gunicorn for Django
CMD ["python", "manage.py", "migrate","&&","gunicorn", "core.wsgi", "--bind", "0.0.0.0:8000"]
