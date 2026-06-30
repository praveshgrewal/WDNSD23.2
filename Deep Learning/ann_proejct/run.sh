#!/bin/bash

# Fraud Detection Django Application - Run Script
# This script activates the tf_env and starts the Django development server

echo "🚨 Fraud Detection - Django Application"
echo "======================================="
echo ""

# Activate the tf_env conda environment
echo "Activating tf_env environment..."
source /opt/anaconda3/bin/activate tf_env

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from the project root directory."
    exit 1
fi

# Apply migrations if needed
echo "Applying database migrations..."
python manage.py migrate

echo ""
echo "✅ Starting development server..."
echo "======================================="
echo "🌐 Access the application at: http://127.0.0.1:8000/"
echo "📊 Admin panel at: http://127.0.0.1:8000/admin/"
echo ""
echo "Press Ctrl+C to stop the server"
echo "======================================="
echo ""

# Start the development server
python manage.py runserver
