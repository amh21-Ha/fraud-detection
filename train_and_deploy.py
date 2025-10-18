#!/usr/bin/env python3
"""
One-click setup script for PythonAnyWhere
Run this once to set up everything
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a shell command and handle errors"""
    print(f"🚀 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def setup_pythonanywhere():
    """Set up the application on PythonAnyWhere"""
    print("🎯 Setting up Fraud Detection API on PythonAnyWhere...")
    
    # Create necessary directories
    directories = ['models', 'static', 'data']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        return False
    
    # Train the model
    if not run_command("python -m app.ml.train_model", "Training ML model"):
        print("⚠️  Model training failed, but continuing with fallback...")
    
    print("🎉 Setup completed successfully!")
    print("\n📝 Next steps on PythonAnyWhere:")
    print("1. Go to the Web tab")
    print("2. Add a new web app")
    print("3. Select 'Manual configuration'")
    print("4. Python version: 3.10+")
    print("5. In WSGI file, point to this project's wsgi.py")
    print("6. Reload your web app")
    print("\n🌐 Your app will be available at: https://yourusername.pythonanywhere.com")

if __name__ == "__main__":
    setup_pythonanywhere()