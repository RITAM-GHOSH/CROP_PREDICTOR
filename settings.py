import streamlit as st
import os
import json
from pathlib import Path

# Constants
SETTINGS_DIR = ".streamlit"
SETTINGS_FILE = "email_settings.json"
SETTINGS_PATH = Path(SETTINGS_DIR) / SETTINGS_FILE

def save_settings(settings):
    """Save settings to JSON file."""
    # Ensure directory exists
    Path(SETTINGS_DIR).mkdir(exist_ok=True)
    
    # Write settings to file
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f)
    
    # Set environment variables
    for key, value in settings.items():
        if value:  # Only set non-empty values
            os.environ[key] = value

def load_settings():
    """Load settings from JSON file."""
    if not SETTINGS_PATH.exists():
        return {
            "EMAIL_USER": "",
            "EMAIL_PASSWORD": "",
            "SMTP_SERVER": "smtp.gmail.com",
            "SMTP_PORT": "587"
        }
    
    with open(SETTINGS_PATH, 'r') as f:
        settings = json.load(f)
    
    # Set environment variables from loaded settings
    for key, value in settings.items():
        if value:  # Only set non-empty values
            os.environ[key] = value
            
    return settings

def settings_page():
    """Render the settings page."""
    st.title("Email Configuration Settings")
    
    # Load current settings
    current_settings = load_settings()
    
    # Create form for settings
    with st.form("email_settings_form"):
        st.subheader("SMTP Email Settings")
        st.info("""
        These settings are required for the email functionality to work. 
        If you're using Gmail, you'll need to use an App Password instead of your regular password.
        """)
        
        # Email user
        email_user = st.text_input(
            "Email Address (Sender)",
            value=current_settings.get("EMAIL_USER", ""),
            help="The email address that will be used to send reports"
        )
        
        # Email password - use password input for security
        email_password = st.text_input(
            "Email Password or App Password", 
            value=current_settings.get("EMAIL_PASSWORD", ""),
            type="password",
            help="For Gmail, use an App Password (generated in your Google Account)"
        )
        
        # Advanced settings - collapsible
        with st.expander("Advanced SMTP Settings"):
            # SMTP Server
            smtp_server = st.text_input(
                "SMTP Server",
                value=current_settings.get("SMTP_SERVER", "smtp.gmail.com"),
                help="The SMTP server address (e.g., smtp.gmail.com for Gmail)"
            )
            
            # SMTP Port
            smtp_port = st.text_input(
                "SMTP Port", 
                value=current_settings.get("SMTP_PORT", "587"),
                help="The SMTP server port (usually 587 for TLS or 465 for SSL)"
            )
        
        # Save button
        submit = st.form_submit_button("Save Settings")
        
        if submit:
            # Collect settings
            settings = {
                "EMAIL_USER": email_user,
                "EMAIL_PASSWORD": email_password,
                "SMTP_SERVER": smtp_server,
                "SMTP_PORT": smtp_port
            }
            
            # Save settings
            save_settings(settings)
            st.success("Settings saved successfully!")
            
            # Provide a test email option
            st.info("You can now test your email configuration by sending a test email.")
    
    # Test email functionality - outside the form
    if os.environ.get("EMAIL_PASSWORD"):
        st.subheader("Test Email Configuration")
        test_email = st.text_input("Enter an email address to send a test message")
        
        if st.button("Send Test Email") and test_email:
            if "@" in test_email:
                with st.spinner("Sending test email..."):
                    try:
                        import smtplib
                        from email.mime.multipart import MIMEMultipart
                        from email.mime.text import MIMEText
                        from email.utils import formatdate
                        
                        # Setup email
                        sender_email = os.environ.get('EMAIL_USER')
                        sender_password = os.environ.get('EMAIL_PASSWORD')
                        
                        msg = MIMEMultipart()
                        msg['From'] = sender_email
                        msg['To'] = test_email
                        msg['Date'] = formatdate(localtime=True)
                        msg['Subject'] = "Test Email from Crop & Fertilizer Recommendation System"
                        
                        # Email body
                        email_body = """
                        Hello,
                        
                        This is a test email from the Crop & Fertilizer Recommendation System.
                        
                        If you received this email, it means your email configuration is working correctly.
                        
                        Regards,
                        Crop & Fertilizer Recommendation System
                        """
                        
                        msg.attach(MIMEText(email_body))
                        
                        # Connect to server and send email
                        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
                        smtp_port = int(os.environ.get('SMTP_PORT', 587))
                        
                        with smtplib.SMTP(smtp_server, smtp_port) as server:
                            server.starttls()
                            server.login(sender_email, sender_password)
                            server.sendmail(sender_email, test_email, msg.as_string())
                        
                        st.success(f"Test email sent successfully to {test_email}!")
                    except Exception as e:
                        st.error(f"Failed to send test email: {str(e)}")
                        st.info("Please check your email settings and try again.")
            else:
                st.error("Please enter a valid email address.")
    else:
        st.warning("Please configure and save your email settings first.")
        
    # Help section
    st.subheader("Help & Troubleshooting")
    with st.expander("Email Configuration Help"):
        st.markdown("""
        ### Gmail Configuration
        
        1. Use your Gmail address as the Email Address
        2. For the password, you need to use an App Password:
           - Go to your Google Account > Security
           - Enable 2-Step Verification if not already enabled
           - Go to App passwords
           - Select "Mail" and "Other (Custom name)"
           - Enter "Crop Adviser" as the name
           - Click "Generate" and use the 16-character password
           
        ### Other Email Providers
        
        For other email providers, you'll need:
        - SMTP server address (e.g., smtp.office365.com for Outlook)
        - SMTP port (usually 587 for TLS or 465 for SSL)
        - Your email address and password
        
        ### Common Issues
        
        - **Authentication Failed**: Check your email and password
        - **Connection Refused**: Check your SMTP server and port
        - **Timeout**: Your network might be blocking SMTP traffic
        """)