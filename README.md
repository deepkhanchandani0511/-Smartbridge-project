# Drishyamitra - AI Powered Photo Management and Delivery System

A complete full-stack application for intelligent photo management powered by AI, face recognition, and natural language processing.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![React](https://img.shields.io/badge/react-18.2-blue)

## 🚀 Features

### Core Features

- **Photo Management**: Upload and organize photos in a responsive gallery
- **Face Recognition**: Automatic face detection and person identification using DeepFace
- **Person Organization**: Group photos by identified people
- **AI Chat Assistant**: Natural language queries powered by Groq API
- **Email Delivery**: Send photos via Gmail SMTP
- **WhatsApp Integration**: Share photos directly via WhatsApp
- **Delivery History**: Track all photo deliveries

### Technology Stack

**Backend:**

- Python 3.11
- Flask - RESTful API framework
- SQLAlchemy - ORM for database operations
- DeepFace - Face detection and recognition
- Groq API - AI Chat Assistant
- JWT - Authentication
- Celery + Redis - Background tasks
- PostgreSQL - Database

**Frontend:**

- React 18.2
- Vite - Build tool
- Tailwind CSS - Styling
- Axios - HTTP client
- React Router - Navigation
- Framer Motion - Animations
- Lucide React - Icons

**Deployment:**

- Docker & Docker Compose
- Nginx - Reverse proxy
- Let's Encrypt - SSL/TLS

## 📋 Prerequisites

- Docker & Docker Compose (v20.10+)
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)
- PostgreSQL 15+ (if running locally)
- Redis 7+ (if running locally)

### API Keys Required

- **Groq API Key**: Get from https://console.groq.com/keys
- **Gmail App Password**: Generate from Google Account settings
- **WhatsApp Web API** (optional): Setup whatsapp-web.js locally

## 🛠️ Installation & Setup

### Option 1: Docker Compose (Recommended)

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/drishyamitra.git
cd drishyamitra
```

#### 2. Setup Environment Files

```bash
# Backend environment
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys

# Frontend environment
cp frontend/.env.example frontend/.env
# Edit frontend/.env with your API URL
```

#### 3. Configure Environment Variables

Edit `backend/.env`:

```env
FLASK_ENV=production
DATABASE_URL=postgresql://drishyamitra_user:drishyamitra_password@postgres:5432/drishyamitra
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
GROQ_API_KEY=your-groq-api-key-here
GMAIL_EMAIL=your-email@gmail.com
GMAIL_PASSWORD=your-gmail-app-password
WHATSAPP_API_URL=http://localhost:3001
```

#### 4. Build and Run with Docker Compose

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# Initialize database (run once)
docker-compose exec backend python -c "from config import init_db; init_db()"

# View logs
docker-compose logs -f
```

Services will be available at:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Nginx**: http://localhost (ports 80/443)

### Option 2: Local Development

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python -c "from config import init_db; init_db()"

# Start server
python start_server.py
```

Server runs on http://localhost:5000

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
# Edit .env with API URL: VITE_API_URL=http://localhost:5000/api

# Start development server
npm run dev
```

Frontend runs on http://localhost:3000

#### Redis & Celery (Optional for background tasks)

```bash
# Start Redis server
redis-server

# In another terminal, start Celery worker
cd backend
celery -A workers.celery_worker worker -l INFO
```

## 📖 API Documentation

### Authentication Endpoints

#### Signup

```
POST /api/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response: 201 Created
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com"
  }
}
```

#### Login

```
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response: 200 OK
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com"
  }
}
```

### Photo Endpoints

#### Upload Photo

```
POST /api/photos/upload
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

file: <image_file>

Response: 201 Created
{
  "message": "Photo uploaded successfully",
  "photo": {
    "id": 1,
    "filename": "20231004_120530_abc12def.jpg",
    "faces_detected": 3
  }
}
```

#### List Photos

```
GET /api/photos/list
Authorization: Bearer <access_token>

Response: 200 OK
{
  "photos": [
    {
      "id": 1,
      "filename": "photo.jpg",
      "upload_date": "2023-10-04T12:05:30",
      "processed": 2
    }
  ]
}
```

#### Delete Photo

```
DELETE /api/photos/<photo_id>
Authorization: Bearer <access_token>

Response: 200 OK
{
  "message": "Photo deleted successfully"
}
```

### Face Recognition Endpoints

#### Process Photo for Faces

```
POST /api/faces/process/<photo_id>
Authorization: Bearer <access_token>

Response: 200 OK
{
  "photo_id": 1,
  "faces_count": 3,
  "faces": [
    {
      "id": 1,
      "person_id": null,
      "person_name": "Unknown",
      "confidence": 0.95
    }
  ]
}
```

#### Label Face

```
PUT /api/faces/<face_id>/label
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "person_name": "John Doe"
}

Response: 200 OK
{
  "message": "Face labeled successfully",
  "face": {
    "id": 1,
    "person_id": 1,
    "person_name": "John Doe"
  }
}
```

#### Get All People

```
GET /api/faces/people
Authorization: Bearer <access_token>

Response: 200 OK
{
  "people_count": 5,
  "people": [
    {
      "id": 1,
      "name": "John Doe",
      "faces_count": 12
    }
  ]
}
```

### Chat Endpoints

#### Send Message

```
POST /api/chat
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "message": "Show photos of John"
}

Response: 200 OK
{
  "response": "Found 5 photos of John.",
  "action": "show_photos",
  "data": [
    {
      "id": 1,
      "filename": "photo1.jpg",
      "upload_date": "2023-10-04T12:05:30"
    }
  ]
}
```

### Delivery Endpoints

#### Send Photo via Email

```
POST /api/delivery/email
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "photo_id": 1,
  "recipient": "friend@example.com"
}

Response: 200 OK
{
  "success": true,
  "delivery_id": 1,
  "message": "Email sent successfully"
}
```

#### Send Photo via WhatsApp

```
POST /api/delivery/whatsapp
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "photo_id": 1,
  "recipient": "+1234567890"
}

Response: 200 OK
{
  "success": true,
  "delivery_id": 2,
  "message": "Photos sent via WhatsApp"
}
```

#### Get Delivery History

```
GET /api/delivery/history
Authorization: Bearer <access_token>

Response: 200 OK
{
  "history": [
    {
      "id": 1,
      "photo_id": 1,
      "method": "email",
      "recipient": "friend@example.com",
      "timestamp": "2023-10-04T12:05:30",
      "status": "sent"
    }
  ],
  "stats": {
    "total": 10,
    "sent": 9,
    "failed": 1,
    "email": 6,
    "whatsapp": 4
  }
}
```

## 🌐 Deployment

### Using Docker Compose

#### 1. Prepare Production Environment

```bash
# Create production .env file
cat > .env << EOF
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)
GROQ_API_KEY=your_groq_api_key
GMAIL_EMAIL=your_email@gmail.com
GMAIL_PASSWORD=your_app_password
EOF
```

#### 2. Generate SSL Certificates

```bash
# Using Let's Encrypt with Certbot
mkdir -p nginx/ssl
certbot certonly --standalone -d your-domain.com

# Copy certificates
cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/cert.pem
cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/key.pem
```

#### 3. Deploy

```bash
# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f

# Create backups cron job
0 2 * * * docker-compose exec -T postgres pg_dump -U drishyamitra_user drishyamitra > /backups/drishyamitra_$(date +\%Y\%m\%d).sql
```

### Cloud Deployment

#### AWS EC2

```bash
# 1. Launch EC2 instance (Ubuntu 22.04)
# 2. Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 3. Clone repository
git clone https://github.com/yourusername/drishyamitra.git
cd drishyamitra

# 4. Configure environment
cp .env.example .env
# Edit .env with your values

# 5. Deploy
docker-compose up -d
```

#### Azure App Service

```bash
# Use Azure Container Registry to push images
# Then deploy using Azure App Service
az containerapp create --resource-group myResourceGroup \
  --name drishyamitra --image myregistry.azurecr.io/drishyamitra:latest
```

## 📚 Project Structure

```
drishyamitra/
├── backend/
│   ├── models/           # SQLAlchemy ORM models
│   ├── routes/           # API route blueprints
│   ├── services/         # Business logic services
│   ├── workers/          # Celery tasks
│   ├── utils/            # Utility functions
│   ├── data/             # Photo uploads & organized folders
│   ├── app.py            # Flask application
│   ├── config.py         # Configuration
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile        # Docker image
├── frontend/
│   ├── src/
│   │   ├── pages/        # React pages
│   │   ├── components/   # Reusable components
│   │   ├── services/     # API client
│   │   ├── context/      # React context
│   │   └── utils/        # Helper functions
│   ├── package.json      # Node dependencies
│   ├── Dockerfile        # Docker image
│   └── vite.config.js    # Vite configuration
├── nginx/
│   ├── nginx.conf        # Nginx configuration
│   └── ssl/              # SSL certificates
├── docker-compose.yml    # Docker Compose configuration
└── README.md             # This file
```

## 🔐 Security Considerations

1. **JWT Authentication**: All API endpoints are protected with JWT tokens
2. **Password Hashing**: Passwords are hashed using bcrypt
3. **HTTPS/SSL**: Enabled in production using Let's Encrypt
4. **CORS**: Configured to allow only specified origins
5. **Rate Limiting**: Nginx limits API and general requests
6. **SQLAlchemy Injection Protection**: All queries use parameterized statements
7. **Environment Variables**: Sensitive data is stored in .env files (not in code)

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run unit tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

## 📊 Database Schema

### Users Table

- id (PK)
- email (UNIQUE)
- password_hash
- created_at
- updated_at

### Photos Table

- id (PK)
- user_id (FK)
- file_path
- filename
- upload_date
- processed (0=pending, 1=processing, 2=completed, -1=failed)
- created_at
- updated_at

### Faces Table

- id (PK)
- photo_id (FK)
- person_id (FK)
- embedding_data (JSON)
- bounding_box
- confidence
- created_at
- updated_at

### People Table

- id (PK)
- user_id (FK)
- name
- description
- created_at
- updated_at

### DeliveryHistory Table

- id (PK)
- user_id (FK)
- photo_id (FK)
- method (email/whatsapp)
- recipient
- timestamp
- status (pending/sent/failed)
- error_message
- created_at
- updated_at

## 🐛 Troubleshooting

### Database Connection Error

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check database connection
docker-compose exec backend python -c "from config import SessionLocal; SessionLocal()"
```

### Face Detection Not Working

- Ensure OpenCV is installed: `pip install opencv-python`
- Check image format and size
- Verify DeepFace models are downloaded: `~/.deepface/weights/`

### Gmail Delivery Issues

- Enable "Less secure app access" or use App Passwords
- Check GMAIL_EMAIL and GMAIL_PASSWORD in .env
- Verify internet connection

### WhatsApp Integration

- Ensure WhatsApp Web API is running on localhost:3001
- Use QR code to authenticate
- Check phone and message recipient format

## 📝 Changelog

### Version 1.0.0 (Initial Release)

- Core photo management
- Face recognition and labeling
- AI chat assistant
- Email and WhatsApp delivery
- Dashboard and gallery views
- Docker deployment setup

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 📞 Support

For issues and questions:

- Open an issue on GitHub
- Check existing documentation
- Review API documentation

## 🙏 Acknowledgments

- DeepFace for face recognition
- Groq for the powerful AI models
- Flask and React communities
- All contributors and users

---

**Made with ❤️ for intelligent photo management**
