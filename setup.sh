#!/bin/bash

# Script to set up the Crop & Fertilizer Recommendation System
# in VS Code or any local environment

echo "Setting up Crop & Fertilizer Recommendation System..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    
    # Check if venv was created successfully
    if [ ! -d "venv" ]; then
        echo "Failed to create virtual environment. Please make sure Python 3 is installed."
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Unix/macOS
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r dependencies.txt

# Create .streamlit directory if it doesn't exist
if [ ! -d ".streamlit" ]; then
    echo "Creating .streamlit directory..."
    mkdir -p .streamlit
fi

# Create config.toml if it doesn't exist
if [ ! -f ".streamlit/config.toml" ]; then
    echo "Creating Streamlit configuration..."
    cat > .streamlit/config.toml << EOL
[server]
headless = true
address = "0.0.0.0"
port = 8501

[theme]
primaryColor = "#4CAF50"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[global]
developmentMode = false

[browser]
gatherUsageStats = false
EOL
fi

echo ""
echo "Setup complete! You can now run the application with:"
echo "streamlit run app.py"
echo ""
echo "The application will be available at http://localhost:8501"