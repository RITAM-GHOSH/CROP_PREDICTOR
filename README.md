# 🌱 Crop & Fertilizer Recommendation System

A data-driven web application that helps farmers make informed decisions about crop selection and fertilizer usage based on environmental conditions and soil analysis.

## Features

- **Crop Recommendations**: Get personalized crop suggestions based on soil and environmental conditions
- **Fertilizer Analysis**: Receive tailored fertilizer recommendations based on soil nutrient levels
- **Interactive Visualizations**: Explore data through intuitive charts and graphs
- **PDF Reports**: Generate and download comprehensive reports
- **Email Integration**: Send reports directly to your email
- **Mobile Responsive**: Optimized for both desktop and mobile devices

## Technology Stack

- **Frontend**: Streamlit
- **Data Analysis**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib
- **Machine Learning**: scikit-learn
- **PDF Generation**: ReportLab
- **Email**: SMTP integration

## Deployment in VS Code

### Prerequisites

- Python 3.10 or higher
- Visual Studio Code
- Git

### Setup Instructions

#### Automatic Setup

For convenient setup, use the provided scripts:

- **On Windows**: Double-click `setup.bat` or run it from Command Prompt
- **On macOS/Linux**: Run `bash setup.sh` in Terminal

These scripts will:
1. Create a virtual environment
2. Install all required dependencies
3. Set up the proper Streamlit configuration

After running the setup script, you can start the application with:
```bash
# Make sure your virtual environment is active
streamlit run app.py
```

#### Manual Setup

If you prefer to set up the application manually:

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd crop-fertilizer-recommendation
   ```

2. **Create a virtual environment**

   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r dependencies.txt
   ```

   If dependencies.txt is not available, install the following packages:
   ```bash
   pip install streamlit pandas numpy matplotlib plotly scikit-learn reportlab python-dotenv
   ```

4. **Configure the application**

   - Ensure the `.streamlit` directory contains the proper configuration files
   - For email functionality:
     - Copy `.env-example` to `.env`
     - Edit `.env` with your email credentials
     - Required variables:
       - `EMAIL_USER`: Your email address
       - `EMAIL_PASSWORD`: Your email password or app password
       - `SMTP_SERVER`: SMTP server (default: smtp.gmail.com)
       - `SMTP_PORT`: SMTP port (default: 587)

5. **Run the application from VS Code**

   - Open VS Code and the project folder
   - Open a terminal in VS Code (Terminal > New Terminal)
   - Make sure your virtual environment is active
   - Run the Streamlit app:
     ```bash
     streamlit run app.py
     ```

6. **Access the application**

   The application will be available at http://localhost:8501 by default

## VS Code Extensions

For the best development experience, install these VS Code extensions:

- **Python**: Microsoft's Python extension
- **Pylance**: Enhanced language server for Python
- **Streamlit**: Provides Streamlit-specific code snippets and support
- **Jupyter**: For working with Jupyter notebooks if needed

## Project Structure

- `app.py`: Main Streamlit application
- `crop_recommendation_model.py`: ML model for crop prediction
- `crop_data.py`: Dataset and agricultural information
- `reportlab_pdf.py`: PDF generation functionality
- `settings.py`: Email and application settings
- `.streamlit/config.toml`: Streamlit configuration
- `setup.sh`: Setup script for macOS/Linux
- `setup.bat`: Setup script for Windows
- `dependencies.txt`: List of required packages
- `.env-example`: Template for environment variables
- `README.md`: This documentation file

## Customization

You can customize the application by modifying the following:

- `.streamlit/config.toml`: Change theme colors, server settings
- `crop_data.py`: Add or modify crop and fertilizer information
- `reportlab_pdf.py`: Customize the PDF report format and content

## Troubleshooting

- **Port issues**: If port 8501 is already in use, Streamlit will automatically try to use another port. Check the terminal output for the URL.
- **Email configuration**: For Gmail, you may need to enable "Less secure app access" or use an App Password.
- **Dependencies**: If you encounter missing dependencies, install them with `pip install [package-name]`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Deployment on Railway

### Prerequisites
- GitHub account
- Railway.app account
- Your project pushed to a GitHub repository

### Deployment Steps

1. **Log in to Railway**

   Go to [Railway.app](https://railway.app/) and log in using your GitHub account or create a new account.

2. **Create a New Project**

   - Click on "New Project"
   - Select "Deploy from GitHub repo"
   - Choose the repository containing this application
   - Click "Deploy Now"

3. **Configure Environment Variables**

   - Go to your project on Railway
   - Navigate to the "Variables" tab
   - Add the following variables if you want to use email functionality:
     - `EMAIL_USER`: Your email address
     - `EMAIL_PASSWORD`: Your email password or app password
     - `SMTP_SERVER`: SMTP server (default: smtp.gmail.com)
     - `SMTP_PORT`: SMTP port (default: 587)

4. **Monitor Deployment**

   - Railway will automatically detect the application as a Python app
   - It will use the requirements.txt file to install dependencies
   - The deployment status can be monitored in the "Deployments" tab

5. **Access Your Application**

   - Once deployed, Railway will provide a URL to access your application
   - Click on the domain name in the "Settings" tab to view your live application

### Troubleshooting Railway Deployment

- **Build Failures**: Check the build logs for errors and ensure all dependencies are correctly listed in requirements.txt
- **Runtime Errors**: Check the logs in the "Deployments" tab for runtime errors
- **Custom Domain**: You can configure a custom domain in the "Settings" tab

## License

[MIT License](LICENSE)
## Deployment on Railway

### Prerequisites
- GitHub account
- Railway.app account
- Your project pushed to a GitHub repository

### Deployment Steps

1. **Log in to Railway**

   Go to [Railway.app](https://railway.app/) and log in using your GitHub account or create a new account.

2. **Create a New Project**

   - Click on "New Project"
   - Select "Deploy from GitHub repo"
   - Choose the repository containing this application
   - Click "Deploy Now"

3. **Configure Environment Variables**

   - Go to your project on Railway
   - Navigate to the "Variables" tab
   - Add the following variables if you want to use email functionality:
     - `EMAIL_USER`: Your email address
     - `EMAIL_PASSWORD`: Your email password or app password
     - `SMTP_SERVER`: SMTP server (default: smtp.gmail.com)
     - `SMTP_PORT`: SMTP port (default: 587)

4. **Monitor Deployment**

   - Railway will automatically detect the application as a Python app
   - It will use the requirements.txt file to install dependencies
   - The deployment status can be monitored in the "Deployments" tab

5. **Access Your Application**

   - Once deployed, Railway will provide a URL to access your application
   - Click on the domain name in the "Settings" tab to view your live application

### Troubleshooting Railway Deployment

- **Build Failures**: Check the build logs for errors and ensure all dependencies are correctly listed in requirements.txt
- **Runtime Errors**: Check the logs in the "Deployments" tab for runtime errors
- **Custom Domain**: You can configure a custom domain in the "Settings" tab
