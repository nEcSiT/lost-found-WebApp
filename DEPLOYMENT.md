# 🚀 Lost & Found Web Application - Deployment Guide

## Overview
This guide will help you deploy the Lost & Found Web Application to various free hosting platforms.

## Prerequisites
- GitHub account
- Project code in GitHub repository
- Team member photos (optional)

## 📋 Deployment Steps

### 1. Prepare Your Repository
Make sure your GitHub repository contains all the files created during setup:
- `requirements.txt` ✅
- `Procfile` ✅ 
- `config.py` ✅
- `.env.example` ✅
- `deploy.sh` ✅

### 2. Choose Your Hosting Platform

#### 🌟 Render (Recommended)
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New Web Service"
4. Connect your repository
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
   - **Environment**: Python 3

#### Environment Variables to Set:
```
SECRET_KEY=your-generated-secret-key
DATABASE_URL=postgresql://... (auto-provided)
FLASK_ENV=production
TWILIO_ACCOUNT_SID=your_sid (optional)
TWILIO_AUTH_TOKEN=your_token (optional)
TWILIO_PHONE_NUMBER=your_number (optional)
```

### 3. Alternative Platforms

#### Railway
1. Go to https://railway.app
2. Sign in with GitHub
3. Deploy from GitHub repository
4. Add PostgreSQL database
5. Set environment variables

#### Heroku
1. Go to https://heroku.com
2. Create new app
3. Connect GitHub repository
4. Add Heroku Postgres add-on
5. Set config vars (environment variables)

#### PythonAnywhere
1. Go to https://pythonanywhere.com
2. Create free account
3. Upload code via Git or file upload
4. Configure web app in Dashboard
5. Set up database (MySQL)

## 🎯 Your Live URLs
After deployment, your app will be available at:
- **Render**: `https://yourapp.onrender.com`
- **Railway**: `https://yourapp.railway.app`
- **Heroku**: `https://yourapp.herokuapp.com`
- **PythonAnywhere**: `https://yourusername.pythonanywhere.com`

## 📸 Adding Team Photos
1. Upload photos to `app/static/images/` folder
2. Name them exactly as specified:
   - `nicholas.jpg`
   - `daniel_eli.jpg`
   - `daniel_adjei.jpg`
   - `nhyiraba.jpg`
   - `kingsley.jpg`

## 🔧 Post-Deployment
1. Visit your live URL
2. Test user registration and login
3. Test item reporting functionality
4. Verify About page displays correctly
5. Check responsive design on mobile

## 🎉 Congratulations!
Your Lost & Found Web Application is now live and accessible to anyone with the URL!

## 📞 Support
If you encounter issues:
1. Check deployment logs on your hosting platform
2. Verify environment variables are set correctly
3. Ensure database is properly initialized

---
**Developed by**: Level 100 Computer Science Students, Accra Technical University
**Team**: Nicholas Dornyo, Daniel Eli Dumedah, Daniel Nana Kojo Ayeyi Adjei, Nhyiraba Agyeman Peprah, Kingsley
