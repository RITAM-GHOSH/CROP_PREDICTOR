@echo off
echo Setting up Crop ^& Fertilizer Recommendation System...

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    
    REM Check if venv was created successfully
    if not exist venv (
        echo Failed to create virtual environment. Please make sure Python 3 is installed.
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r dependencies.txt

REM Create .streamlit directory if it doesn't exist
if not exist .streamlit (
    echo Creating .streamlit directory...
    mkdir .streamlit
)

REM Create config.toml if it doesn't exist
if not exist .streamlit\config.toml (
    echo Creating Streamlit configuration...
    (
        echo [server]
        echo headless = true
        echo address = "0.0.0.0"
        echo port = 8501
        echo.
        echo [theme]
        echo primaryColor = "#4CAF50"
        echo backgroundColor = "#FFFFFF"
        echo secondaryBackgroundColor = "#F0F2F6"
        echo textColor = "#262730"
        echo.
        echo [global]
        echo developmentMode = false
        echo.
        echo [browser]
        echo gatherUsageStats = false
    ) > .streamlit\config.toml
)

echo.
echo Setup complete! You can now run the application with:
echo streamlit run app.py
echo.
echo The application will be available at http://localhost:8501