FROM python:3.12-slim

# Install system dependencies needed for WeasyPrint and PostgreSQL
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libpango1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libjpeg-dev \
    libpng-dev \
    libpq-dev \
    postgresql-client \
    git \
    curl \
    libglib2.0-dev \
    && rm -rf /var/lib/apt/lists/*


# Set working directory inside container
WORKDIR /app

# Copy requirements file first (for better caching)
COPY requirements.txt .

# Install Python dependencies including WeasyPrint
RUN pip install -r requirements.txt

# Copy all project files
COPY . .

# Expose port 8000 for Django
EXPOSE 8000

# Command to run when container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]