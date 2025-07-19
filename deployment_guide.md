# WebDev4U - Deployment Guide

**Live Application**: https://milestone-project-4-ecommerce-479bb413016e.herokuapp.com/

## System Requirements & Setup

### Required Software
- Python 3.12+
- Docker Desktop
- Git
- PostgreSQL (for local development)

### Installation Verification
```powershell
python --version
docker --version
docker-compose --version
git --version
```

## Environment Configuration

### 1. Clone Repository
```powershell
git clone https://github.com/Jere-The-Hutt/milestone-project-4-ecommerce.git
cd milestone-project-4-ecommerce
```

### 2. Setup Environment Variables
```powershell
# Copy environment template
Copy-Item env.py env_local.py
```

Edit `env_local.py`:
```python
import os

# Core Settings
os.environ["SECRET_KEY"] = "your-super-secret-key-here"
os.environ["DEBUG"] = "True"  # False for production

# Database (Code Institute provided)
os.environ["DATABASE_URL"] = "your-database-url-here"

# Cloudinary
os.environ['CLOUDINARY_CLOUD_NAME'] = 'your-cloud-name'
os.environ['CLOUDINARY_API_KEY'] = 'your-api-key'
os.environ['CLOUDINARY_API_SECRET'] = 'your-api-secret'

# Stripe (Test/Live Keys)
os.environ['STRIPE_PUBLISHABLE_KEY'] = 'pk_test_your_publishable_key'
os.environ['STRIPE_SECRET_KEY'] = 'sk_test_your_secret_key'
os.environ['STRIPE_WEBHOOK_SECRET'] = 'whsec_your_webhook_secret'

# Email Configuration
os.environ['EMAIL_HOST_USER'] = 'your-email@gmail.com'
os.environ['EMAIL_HOST_PASSWORD'] = 'your-app-password'  # Gmail App Password
os.environ['DEFAULT_FROM_EMAIL'] = 'WebDev4U <your-email@gmail.com>'
```

## Deployment Options

### Option 1: Docker Deployment (Recommended)
```powershell
# Build and start services
docker-compose build
docker-compose up -d

# Setup database
docker-compose exec django python manage.py migrate
docker-compose exec django python manage.py createsuperuser
docker-compose exec django python manage.py collectstatic --noinput

# View logs
docker-compose logs -f
```

### Option 2: Virtual Environment
```powershell
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies and setup
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Access Points
- **Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/
- **RabbitMQ Management**: http://localhost:15672 (guest/guest)

## Testing & Verification

### Service Health Check
```powershell
# Check Docker services
docker-compose ps

# Test application endpoints
curl http://localhost:8000
curl http://localhost:8000/admin/
```

### Payment Testing (Stripe Test Mode)
- **Successful Payment**: 4242 4242 4242 4242
- **Declined Payment**: 4000 0000 0000 0002
- **Requires Authentication**: 4000 0025 0000 3155

Use any future expiry date and any 3-digit CVC.

## Production Deployment (Heroku)

### Prerequisites
- Heroku CLI installed
- Heroku account with app created

### Environment Setup
```powershell
# Login to Heroku
heroku login

# Set production environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY="your-production-secret-key"
heroku config:set DATABASE_URL="your-production-database-url"
heroku config:set CLOUDINARY_CLOUD_NAME="your-cloud-name"
heroku config:set CLOUDINARY_API_KEY="your-api-key"
heroku config:set CLOUDINARY_API_SECRET="your-api-secret"
heroku config:set STRIPE_PUBLISHABLE_KEY="pk_live_your_live_key"
heroku config:set STRIPE_SECRET_KEY="sk_live_your_live_key"
heroku config:set EMAIL_HOST_USER="your-email@gmail.com"
heroku config:set EMAIL_HOST_PASSWORD="your-app-password"

# Deploy application
git push heroku main

# Setup database
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Background Tasks (if using Celery)
```powershell
# Add CloudAMQP for RabbitMQ
heroku addons:create cloudamqp:lemur

# Scale worker dynos
heroku ps:scale worker=1
```

## Common Issues & Solutions

### Docker Services Won't Start
```powershell
# Check Docker is running and restart services
docker-compose down
docker-compose up -d

# Check for port conflicts
netstat -an | findstr :8000
```

### Database Connection Issues
```powershell
# Test database connectivity
docker-compose exec django python manage.py check --database default

# Apply migrations if needed
docker-compose exec django python manage.py migrate
```

### Email/Payment Not Working
```powershell
# Verify environment variables are loaded
docker-compose exec django python manage.py shell
# In shell: from django.conf import settings; print(settings.EMAIL_HOST_USER)

# Test email functionality
# In shell: from django.core.mail import send_mail
# send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
```

### Static Files Issues
```powershell
# Recollect static files
docker-compose exec django python manage.py collectstatic --noinput --clear
```

### View Logs for Debugging
```powershell
# View application logs
docker-compose logs django

# View real-time logs
docker-compose logs -f django

# View all service logs
docker-compose logs
```

## Quick Reference

### Full Local Deployment
```powershell
# Clone and setup
git clone https://github.com/Jere-The-Hutt/milestone-project-4-ecommerce.git
cd milestone-project-4-ecommerce
Copy-Item env.py env_local.py
# Edit env_local.py with your credentials

# Deploy with Docker
docker-compose build
docker-compose up -d
docker-compose exec django python manage.py migrate
docker-compose exec django python manage.py createsuperuser

# Access application: http://localhost:8000
```

### Production Deployment to Heroku
```powershell
# Set environment variables and deploy
heroku config:set DEBUG=False SECRET_KEY="your-key" DATABASE_URL="your-db-url"
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

---

**Repository**: https://github.com/Jere-The-Hutt/milestone-project-4-ecommerce  
**Support**: hallu.huttunen@gmail.com