# MongoDB Setup Guide for Shastika Flask App

## Prerequisites
- Python 3.8+
- pip package manager
- A MongoDB Atlas account (cloud) or local MongoDB installation

## Installation Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and update with your credentials:
```bash
cp .env.example .env
```

Edit `.env` file with your MongoDB connection details:
```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?appName=appname
FLASK_SECRET_KEY=your-secret-key-here
ADMIN_EMAIL=admin@example.com
ADMIN_PASS=your-admin-password
```

### 3. Run the Application
```bash
python app.py
```

The app will connect to MongoDB automatically on startup.

## Database Collections

### contact_messages
Stores contact form submissions:
- `name` - Visitor name
- `email` - Email address
- `phone` - Phone number
- `subject` - Message subject
- `message` - Message content

### product_enquiries
Stores product inquiries:
- `product` - Product name
- `name` - Inquirer name
- `country` - Country
- `phone` - Phone number
- `email` - Email address

## API Endpoints

### POST /submit_contact
Submit contact form data

### POST /submit_enquiry
Submit product inquiry

### POST /admin_login
Admin authentication (requires email and password)

### GET /admin/messages
Retrieve all contact messages (requires admin session)

### GET /admin/enquiries
Retrieve all product inquiries (requires admin session)

## Troubleshooting

**"MongoDB connection failed"**
- Check your MONGO_URI in `.env`
- Verify internet connection
- Check MongoDB Atlas IP whitelist settings

**"Database unavailable" error on submissions**
- MongoDB connection failed during startup
- Check app console logs for connection errors
- Verify credentials and network connectivity

**Port already in use**
- Change DEBUG mode or port in app.py
- Kill process using port 5000 (Windows: `netstat -ano | findstr :5000`)
