# Quick Setup Guide

## 🚀 Fastest Setup (5 minutes)

### Prerequisites

- Docker and Docker Compose installed
- API keys ready (Groq, Gmail)

### Step 1: Clone and Configure

```bash
# Clone repository
git clone https://github.com/yourusername/drishyamitra.git
cd drishyamitra

# Copy example environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### Step 2: Add Your API Keys

Edit `backend/.env`:

```bash
GROQ_API_KEY=xxxxxxxxxxxx
GMAIL_EMAIL=your-email@gmail.com
GMAIL_PASSWORD=your-app-password
```

### Step 3: Start Services

```bash
# Build and start all services
docker-compose up -d

# Wait for services to start (30-60 seconds)
docker-compose ps

# Check logs if needed
docker-compose logs -f
```

### Step 4: Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Health**: http://localhost:5000/api/health

### Step 5: Create Account

1. Go to http://localhost:3000
2. Click "Sign Up"
3. Create account with email and password
4. Login

## 📱 First Actions

### 1. Upload a Photo

- Click "Gallery" in navigation
- Upload a test photo (JPG, PNG)
- Wait for face detection to complete

### 2. Label Faces

- Click on detected face in photo
- Enter the person's name
- Save

### 3. Try Chat

- Go to "Chat" page
- Try: "Show photos of [person name]"
- Try: "Send photos to email@example.com"

### 4. Share Photos

- In Gallery, click on photo
- Choose "Share" option
- Select delivery method (Email or WhatsApp)

## ⚙️ Configuration

### Environment Variables

**Backend (.env)**

```env
# Server
FLASK_ENV=production
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Database
DATABASE_URL=postgresql://user:password@postgres:5432/drishyamitra
# Or for local testing: sqlite:///drishyamitra.db

# Security
SECRET_KEY=generate-random-key-here
JWT_SECRET_KEY=generate-random-key-here

# APIs
GROQ_API_KEY=your-key-from-console.groq.com
GMAIL_EMAIL=your-email@gmail.com
GMAIL_PASSWORD=app-password-from-google
WHATSAPP_API_URL=http://localhost:3001  # Optional

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

**Frontend (.env)**

```env
VITE_API_URL=http://localhost:5000/api
```

## 🔍 Verify Installation

### Check All Services Running

```bash
docker-compose ps
```

All services should show `Up`:

- postgres (healthy)
- redis (healthy)
- backend (running)
- celery (running)
- frontend (running)
- nginx (running)

### Test API Endpoint

```bash
# Health check
curl http://localhost:5000/api/health

# Response should be:
# {"status":"ok","timestamp":"...","service":"Drishyamitra API"}
```

### Check Database

```bash
# Connect to database
docker-compose exec postgres psql -U drishyamitra_user -d drishyamitra

# List tables
\dt

# Exit
\q
```

## 🆘 Common Issues

### Port Already in Use

```bash
# Change ports in docker-compose.yml
# For example, use 8000 for frontend:
# ports:
#   - "8000:3000"
```

### Out of Memory

```bash
# Increase Docker memory limit
# In Docker Desktop: Preferences > Resources
# Set Memory to at least 4GB
```

### Database Connection Failed

```bash
# Restart database service
docker-compose restart postgres

# Reinitialize if needed
docker-compose exec backend python -c "from config import init_db; init_db()"
```

### Frontend Doesn't Load

```bash
# Check frontend logs
docker-compose logs frontend

# Restart frontend service
docker-compose restart frontend
```

### API Requests Failing

```bash
# Check backend logs
docker-compose logs backend

# Verify API is running
curl -v http://localhost:5000/api/health
```

## 📝 Development Mode

### Run Backend Locally

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure .env
cp .env.example .env

# Run server
python start_server.py

# Server runs on http://localhost:5000
```

### Run Frontend Locally

```bash
cd frontend

# Install dependencies
npm install

# Configure .env
cp .env.example .env

# Start dev server
npm run dev

# Frontend runs on http://localhost:3000
```

### Run Celery Worker

```bash
cd backend

# Make sure virtualenv is activated
celery -A workers.celery_worker worker -l INFO
```

## 🗄️ Database Management

### Backup Database

```bash
# Automatic backups (in docker-compose)
docker-compose exec -T postgres pg_dump -U drishyamitra_user drishyamitra > backup.sql
```

### Restore Database

```bash
cat backup.sql | docker-compose exec -T postgres psql -U drishyamitra_user drishyamitra
```

### Reset Database

```bash
docker-compose down -v  # Removes all volumes
docker-compose up -d    # Recreates fresh database
```

## 🔐 Production Deployment

### Generate Strong Keys

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Generate JWT_SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"
```

### Setup SSL Certificate

```bash
# Using Let's Encrypt
sudo certbot certonly --standalone -d yourdomain.com

# Copy to nginx/ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/key.pem
```

### Deploy to Server

```bash
# SSH into server
ssh user@your-server.com

# Clone repository
git clone https://github.com/yourusername/drishyamitra.git
cd drishyamitra

# Create .env with production values
nano .env

# Start services
docker-compose up -d

# Check status
docker-compose ps
```

## 📊 Monitoring

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Resource Usage

```bash
docker stats
```

### Database Metrics

```bash
# Connect to database
docker-compose exec postgres psql -U drishyamitra_user drishyamitra

# Check table sizes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables WHERE schemaname != 'pg_catalog' ORDER BY pg_total_relation_size DESC;
```

## 🧹 Cleanup

### Stop All Services

```bash
docker-compose down
```

### Remove All Data (⚠️ Warning)

```bash
docker-compose down -v
```

### Clean Up Docker

```bash
# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove everything (careful!)
docker system prune -a
```

## 📚 Next Steps

1. **Read Full Documentation**: See [README.md](README.md)
2. **API Documentation**: Check [README.md#api-documentation](README.md#api-documentation)
3. **Customization**: Modify colors and settings
4. **Deployment**: Follow deployment guide
5. **Integration**: Add your own AI models or services

## 💡 Tips

- Use `docker-compose logs -f service_name` to debug issues
- Access PostgreSQL directly: `docker-compose exec postgres psql -U drishyamitra_user -d drishyamitra`
- View Redis data: `docker-compose exec redis redis-cli`
- Monitor Celery tasks: `docker-compose exec backend celery -A workers.celery_worker events`

## 🆘 Get Help

- Check logs: `docker-compose logs -f`
- Test API: `curl http://localhost:5000/api/health`
- Read documentation
- Open an issue on GitHub

---

**Got it working? Great! Now explore and customize your Drishyamitra instance!**
