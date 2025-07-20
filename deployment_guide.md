# WebDev4U - Deployment Guide

**Live Application**: https://milestone-project-4-ecommerce-479bb413016e.herokuapp.com/

## System Requirements & Setup

### Required Software
- Python 3.12+
- Docker Desktop
- Git
- PostgreSQL (for local development)
- Visual Studio Code (recommended)

### System Dependencies for PDF Generation
The project uses **WeasyPrint** for PDF generation, which requires specific system libraries:
- `libpango1.0-0`, `libpangocairo-1.0-0`, `libcairo2` (rendering)
- `libjpeg-dev`, `libpng-dev` (image processing)
- `libffi-dev`, `libglib2.0-dev` (core libraries)
- `build-essential` (compilation tools)

**Note**: These dependencies are automatically handled by Docker, but would need manual installation for local Python development.

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
You should already have an `env.py` file in your project root. If you need to create a separate local configuration, you can copy it:

```powershell
# Optional: Create a separate local environment file
Copy-Item env.py env_local.py
```

Your `env.py` file should contain:
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

## Local Development Requirements

**⚠️ IMPORTANT**: This project requires Docker Compose for local development due to:
- **PDF generation** using WeasyPrint (requires system libraries)
- **Custom admin order views** that generate PDF reports
- **Background task processing** with Celery workers
- **Message broker** (RabbitMQ) for task queuing
- **Service coordination** between Django, Celery, and RabbitMQ

Running `python manage.py runserver` alone **will not work properly** without:
1. WeasyPrint system dependencies (libpango, libcairo, etc.)
2. RabbitMQ message broker
3. Celery worker process

### Docker Services Architecture
The project runs three interconnected services:
- **django**: Main web application (Python 3.12-slim, port 8000)
- **celery**: Background task worker for PDF generation
- **rabbitmq**: Message broker with management UI (ports 5672, 15672)

### Docker Deployment (Required)
```powershell
# Build and start all required services
docker-compose build
docker-compose up -d

# Setup database
docker-compose exec django python manage.py migrate
docker-compose exec django python manage.py createsuperuser
docker-compose exec django python manage.py collectstatic --noinput

# View logs
docker-compose logs -f
```

### Alternative: Virtual Environment (Limited Functionality)
```powershell
# ⚠️ WARNING: This setup will have limited functionality
# PDF generation requires WeasyPrint system dependencies
# Background tasks require RabbitMQ and Celery worker

# On Windows, you would need to manually install:
# - Visual Studio Build Tools
# - GTK+ libraries for WeasyPrint
# - RabbitMQ server

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Note: Admin order PDF generation will likely fail
```

### Access Points
- **Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/
- **RabbitMQ Management**: http://localhost:15672 (guest/guest)

### Service Status Check
```powershell
# Check all services are running
docker-compose ps

# Should show:
# - django (running on port 8000)
# - celery (worker process)
# - rabbitmq (running on ports 5672, 15672)
```

## Testing & Verification

### Service Health Check
```powershell
# Check all Docker services are running
docker-compose ps

# Test application endpoints
curl http://localhost:8000
curl http://localhost:8000/admin/

# Check Celery worker is processing tasks
docker-compose logs celery

# Access RabbitMQ management interface
# Go to http://localhost:15672 (login: guest/guest)
```

### Payment Testing (Stripe Test Mode)
- **Successful Payment**: 4242 4242 4242 4242
- **Declined Payment**: 4000 0000 0000 0002
- **Requires Authentication**: 4000 0025 0000 3155

Use any future expiry date and any 3-digit CVC.

## Production Deployment (Heroku Dashboard)

### Prerequisites
- Heroku account (sign up at https://heroku.com)
- GitHub account with your repository
- All project files committed and pushed to GitHub

### Step 1: Create Heroku App
1. Login to your Heroku Dashboard (https://dashboard.heroku.com)
2. Click **"New"** → **"Create new app"**
3. Enter app name (e.g., `your-project-name`)
4. Select region closest to your target users
5. Click **"Create app"**

### Step 2: Configure Environment Variables
In your Heroku app dashboard:

1. Go to **Settings** tab
2. Click **"Reveal Config Vars"**
3. Add the following key-value pairs:

| Key | Value |
|-----|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | `your-production-secret-key` |
| `DATABASE_URL` | `your-production-database-url` |
| `CLOUDINARY_CLOUD_NAME` | `your-cloud-name` |
| `CLOUDINARY_API_KEY` | `your-api-key` |
| `CLOUDINARY_API_SECRET` | `your-api-secret` |
| `STRIPE_PUBLISHABLE_KEY` | `pk_live_your_live_key` |
| `STRIPE_SECRET_KEY` | `sk_live_your_live_key` |
| `STRIPE_WEBHOOK_SECRET` | `whsec_your_webhook_secret` |
| `EMAIL_HOST_USER` | `your-email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | `your-app-password` |
| `DEFAULT_FROM_EMAIL` | `WebDev4U <your-email@gmail.com>` |

### Step 3: Add Required Add-ons
1. **Database**: In **Resources** tab, search for **"Heroku Postgres"**
   - Select a plan (Mini $5/month or free alternatives)
   - Click **"Submit Order Form"**
   - The `DATABASE_URL` will be automatically added to Config Vars

2. **Message Broker**: Search for **"CloudAMQP"**
   - Select **"CloudAMQP"** add-on
   - Choose **"Little Lemur"** plan (free)
   - Click **"Submit Order Form"**
   - The `CLOUDAMQP_URL` will be automatically added to Config Vars

**Note**: No additional buildpacks are required - Heroku's default Python buildpack handles WeasyPrint dependencies automatically.

### Step 4: Connect GitHub Repository
1. Go to **Deploy** tab
2. In **Deployment method**, select **"GitHub"**
3. Click **"Connect to GitHub"** and authorize if prompted
4. Search for your repository name
5. Click **"Connect"** next to your repository

### Step 5: Deploy Application
**Option A: Automatic Deployment**
1. Scroll to **"Automatic deploys"**
2. Select the branch to deploy (usually `main`)
3. Click **"Enable Automatic Deploys"**
4. Click **"Deploy Branch"** for initial deployment

**Option B: Manual Deployment**
1. Scroll to **"Manual deploy"**
2. Select the branch to deploy
3. Click **"Deploy Branch"**

### Step 6: Setup Database and Admin
After successful deployment:

1. Go to **More** menu → **"Run console"**
2. Run database migrations:
   ```bash
   python manage.py migrate
   ```
3. Create superuser account:
   ```bash
   python manage.py createsuperuser
   ```
4. Collect static files (if needed):
   ```bash
   python manage.py collectstatic --noinput
   ```

### Step 7: Configure Stripe Webhooks (Production)
1. Login to your Stripe Dashboard
2. Go to **Developers** → **Webhooks**
3. Click **"Add endpoint"**
4. Enter endpoint URL: `https://your-app-name.herokuapp.com/checkout/wh/`
5. Select events to send
6. Copy the webhook signing secret
7. Add it to Heroku Config Vars as `STRIPE_WEBHOOK_SECRET`

### Step 8: Enable Worker Dyno for Background Tasks
1. Go to **Resources** tab
2. You should see both:
   - **web** dyno (automatically enabled)
   - **worker** dyno (needs to be enabled)
3. Click the toggle/edit button next to **worker**
4. Scale it to **1 dyno**
5. Click **"Confirm"**

This enables the Celery worker process for PDF generation and other background tasks.

## Monitoring & Maintenance

### View Application Logs
1. In your Heroku app dashboard
2. Click **"More"** → **"View logs"**
3. For real-time logs, use the web terminal or enable log streaming

### Update Application
1. Push changes to your GitHub repository
2. If automatic deploys are enabled, deployment happens automatically
3. For manual deployment, go to **Deploy** tab → **"Deploy Branch"**

### Scale Dynos (if needed)
1. Go to **Resources** tab
2. Click the edit icon next to **"web"**
3. Adjust the dyno slider
4. Click **"Confirm"**

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

### Heroku Deployment Issues
1. **Build Fails**: Check build logs in Activity tab
2. **App Crashes**: Check logs for error messages
3. **Config Vars**: Ensure all environment variables are properly set
4. **Static Files**: Make sure `DISABLE_COLLECTSTATIC=1` is NOT set in Config Vars

### Email/Payment Not Working
```powershell
# For local testing - verify environment variables are loaded
docker-compose exec django python manage.py shell
# In shell: from django.conf import settings; print(settings.EMAIL_HOST_USER)

# Test email functionality
# In shell: from django.core.mail import send_mail
# send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
```

### Static Files Issues
```powershell
# For local development - recollect static files
docker-compose exec django python manage.py collectstatic --noinput --clear
```

### View Local Logs for Debugging
```powershell
# View application logs
docker-compose logs django

# View real-time logs
docker-compose logs -f django

# View all service logs
docker-compose logs
```

## Quick Reference

### Full Local Deployment (Required for Full Functionality)
```powershell
# Clone and setup
git clone https://github.com/Jere-The-Hutt/milestone-project-4-ecommerce.git
cd milestone-project-4-ecommerce
# Edit env.py with your credentials

# Deploy with Docker (required for PDF generation and admin features)
docker-compose build
docker-compose up -d
docker-compose exec django python manage.py migrate
docker-compose exec django python manage.py createsuperuser

# Access application: http://localhost:8000
# Admin with PDF features: http://localhost:8000/admin/
```

### Production Deployment Summary
1. Create Heroku app via Dashboard
2. Set all Config Vars (environment variables)
3. Connect GitHub repository
4. Enable automatic or manual deployment
5. Run database setup commands via console
6. Configure Stripe webhooks for production URL

### VSCode + PowerShell Development Setup
```powershell
# Open project in VSCode
code .

# Use integrated PowerShell terminal (Ctrl + `)
# Activate virtual environment if using Option 2
.venv\Scripts\activate

# Run development server
python manage.py runserver
```

---

**Repository**: https://github.com/Jere-The-Hutt/milestone-project-4-ecommerce  
**Live Application**: https://milestone-project-4-ecommerce-479bb413016e.herokuapp.com/  
**Support**: jerethehutt@gmail.com