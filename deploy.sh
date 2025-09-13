#!/bin/bash

# Deployment script for Lost & Found Web Application
echo "🚀 Starting deployment setup..."

# Create uploads directory
mkdir -p app/static/uploads
mkdir -p app/static/images

# Set environment variables (example)
export FLASK_ENV=production
export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')

# Initialize database
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('✅ Database initialized successfully')
"

echo "✅ Deployment setup complete!"
echo "📝 Don't forget to:"
echo "   1. Set environment variables on your hosting platform"
echo "   2. Upload team photos to app/static/images/"
echo "   3. Configure Twilio credentials (optional)"
