import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import os
from crop_recommendation_model import train_model, predict_crop
from crop_data import crop_info, get_dataset, fertilizer_info, recommend_fertilizer
from reportlab_pdf import create_pdf_report
from settings import load_settings, settings_page

# Load email settings
load_settings()

# Set page configuration
st.set_page_config(
    page_title="Crop & Fertilizer Recommendation System",
    page_icon="🌱",
    layout="wide"
)

# Page navigation in sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Settings"])

if page == "Home":
    # App title and description
    st.title("🌱 Crop & Fertilizer Recommendation System")
    st.write("""
    This application helps farmers optimize their agricultural practices with:

    1. **Crop Recommendations**: Determine the optimal crops to plant based on local environmental conditions
    2. **Fertilizer Recommendations**: Get personalized fertilizer advice based on soil nutrient levels and selected crops
    3. **Soil Analysis**: Visualize soil nutrient deficiencies with interactive charts
    4. **PDF Reports**: Download comprehensive reports for offline reference and sharing

    Enter your field's characteristics in the sidebar to receive personalized recommendations.
    """)

# Initialize variables to avoid "possibly unbound" errors
submit_button = False
soil_type = "Loamy"
n_value = 50
p_value = 50
k_value = 50
temperature = 25.0
humidity = 65.0
ph_value = 6.5
rainfall = 100.0

# Only display field conditions form on the Home page
if page == "Home":
    # Create sidebar for inputs
    st.sidebar.header("Field Conditions")

    # Input form for environmental conditions
    with st.sidebar.form("input_form"):
        # Soil type selection
        soil_type = st.selectbox(
            "Soil Type",
            options=["Clay", "Sandy", "Loamy", "Black", "Red", "Clayey"],
            help="Select the type of soil in your field"
        )
    
        # Numerical inputs with appropriate ranges
        n_value = st.slider("Nitrogen (N) Content (kg/ha)", 0, 140, 50, help="Amount of nitrogen in the soil")
        p_value = st.slider("Phosphorus (P) Content (kg/ha)", 5, 145, 50, help="Amount of phosphorus in the soil")
        k_value = st.slider("Potassium (K) Content (kg/ha)", 5, 205, 50, help="Amount of potassium in the soil")
        
        # Temperature input
        temperature = st.slider("Temperature (°C)", 8.0, 44.0, 25.0, help="Average temperature in your area")
        
        # Humidity input
        humidity = st.slider("Humidity (%)", 14.0, 100.0, 65.0, help="Average humidity percentage in your area")
        
        # pH input
        ph_value = st.slider("pH Value", 3.5, 10.0, 6.5, help="pH level of your soil")
        
        # Rainfall input
        rainfall = st.slider("Rainfall (mm)", 20.0, 300.0, 100.0, help="Average rainfall in your area")
        
        # Submit button
        submit_button = st.form_submit_button("Get Recommendations")

# Main area for displaying results
if page == "Home" and submit_button:
    # Show a spinner while processing
    with st.spinner("Analyzing your field conditions..."):
        # Load and train the model
        model, label_encoder = train_model()
        
        # Prepare input data for prediction
        input_data = np.array([[n_value, p_value, k_value, temperature, humidity, ph_value, rainfall]])
        
        # Make prediction with probabilities
        predictions, probabilities = predict_crop(model, label_encoder, input_data)
        
        # Get top 3 recommendations
        top_indices = np.argsort(probabilities[0])[::-1][:3]
        top_crops = [label_encoder.inverse_transform([idx])[0] for idx in top_indices]
        top_probs = [probabilities[0][idx] * 100 for idx in top_indices]
        
        # Display results
        st.header("Recommended Crops")
        
        # Create columns for top recommendations
        cols = st.columns(3)
        
        for i, (crop, prob) in enumerate(zip(top_crops, top_probs)):
            with cols[i]:
                st.subheader(f"{i+1}. {crop}")
                st.metric("Confidence", f"{prob:.1f}%")
                
                # Display crop information
                if crop in crop_info:
                    info = crop_info[crop]
                    st.write(f"**Description:** {info['description']}")
                    st.write(f"**Growing Season:** {info['growing_season']}")
                    st.write(f"**Ideal Conditions:**")
                    st.write(f"- Temperature: {info['ideal_temp']}")
                    st.write(f"- Soil pH: {info['ideal_ph']}")
                    st.write(f"- Water Needs: {info['water_needs']}")
        
        # Visualization section
        st.header("Visualization")
        
        # Create a bar chart for probabilities
        fig = px.bar(
            x=[crop for crop in top_crops],
            y=[prob for prob in top_probs],
            labels={'x': 'Crop', 'y': 'Confidence (%)'},
            title='Top Crop Recommendations',
            color=top_probs,
            color_continuous_scale='Viridis',
        )
        st.plotly_chart(fig)
        
        # Display a radar chart for input conditions
        categories = ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH', 'Rainfall']
        
        # Normalize values for better visualization
        normalized_values = [
            n_value/140, p_value/145, k_value/205, 
            (temperature-8)/(44-8), humidity/100, 
            (ph_value-3.5)/(10-3.5), rainfall/300
        ]
        
        fig = px.line_polar(
            r=normalized_values,
            theta=categories,
            line_close=True,
            title="Your Field Conditions",
        )
        fig.update_traces(fill='toself')
        st.plotly_chart(fig)
        
        # Show environmental condition analysis
        st.header("Environmental Condition Analysis")
        
        # Create a comparison table
        comparison_data = []
        for crop in top_crops:
            if crop in crop_info:
                info = crop_info[crop]
                comparison_data.append({
                    "Crop": crop,
                    "Your Temperature": f"{temperature}°C",
                    "Ideal Temperature": info['ideal_temp'],
                    "Your pH": f"{ph_value}",
                    "Ideal pH": info['ideal_ph'],
                    "Your Rainfall": f"{rainfall} mm",
                    "Water Needs": info['water_needs']
                })
        
        if comparison_data:
            st.table(pd.DataFrame(comparison_data))
            
        # Fertilizer recommendation section
        st.header("Fertilizer Recommendations")
        
        # Get fertilizer recommendations for the top crop
        if top_crops:
            top_crop = top_crops[0]
            fertilizer_recs = recommend_fertilizer(n_value, p_value, k_value, top_crop)
            
            st.write(f"Based on your soil nutrient levels and the recommended crop ({top_crop}), we suggest:")
            
            # Create columns for fertilizer recommendations
            fert_cols = st.columns(len(fertilizer_recs))
            
            for i, rec in enumerate(fertilizer_recs):
                with fert_cols[i]:
                    st.subheader(rec["fertilizer"])
                    st.write(rec["rationale"])
                    
                    # Display fertilizer details if available in our database
                    if rec["fertilizer"] in fertilizer_info:
                        fert_data = fertilizer_info[rec["fertilizer"]]
                        st.write("**Details:**")
                        st.write(f"- {fert_data['description']}")
                        st.write(f"- N-P-K Content: {fert_data['n_content']}-{fert_data['p_content']}-{fert_data['k_content']}")
                        st.write(f"- Recommended application: {fert_data['application_rate']}")
                        st.write(f"- Best time to apply: {fert_data['best_time']}")
            
            # Show NPK deficiency visualization
            st.subheader("Soil Nutrient Analysis")
            
            # Define optimal NPK levels for the recommended crop
            optimal_levels = {"N": 80, "P": 40, "K": 40}
            if top_crop in ["rice", "maize", "wheat"]:
                optimal_levels = {"N": 120, "P": 60, "K": 50}
            elif top_crop in ["vegetables", "tomato", "potato", "cabbage"]:
                optimal_levels = {"N": 100, "P": 80, "K": 80}
            
            # Calculate deficiency percentages
            n_deficit_pct = max(0, 100 * (1 - (n_value / optimal_levels["N"])))
            p_deficit_pct = max(0, 100 * (1 - (p_value / optimal_levels["P"])))
            k_deficit_pct = max(0, 100 * (1 - (k_value / optimal_levels["K"])))
            
            # Create a bar chart for nutrient deficiencies
            nutrient_df = pd.DataFrame({
                "Nutrient": ["Nitrogen (N)", "Phosphorus (P)", "Potassium (K)"],
                "Current Level": [n_value, p_value, k_value],
                "Optimal Level": [optimal_levels["N"], optimal_levels["P"], optimal_levels["K"]],
                "Deficiency (%)": [n_deficit_pct, p_deficit_pct, k_deficit_pct]
            })
            
            # Create two columns for visualization
            nutrient_cols = st.columns(2)
            
            with nutrient_cols[0]:
                # Bar chart comparing current vs optimal
                fig = px.bar(
                    nutrient_df,
                    x="Nutrient",
                    y=["Current Level", "Optimal Level"],
                    barmode="group",
                    title=f"Soil Nutrient Levels for {top_crop}",
                    color_discrete_sequence=["#1E88E5", "#FFC107"]
                )
                st.plotly_chart(fig)
            
            with nutrient_cols[1]:
                # Pie chart showing deficiency percentage
                if any([n_deficit_pct > 0, p_deficit_pct > 0, k_deficit_pct > 0]):
                    # Only nutrients with deficiency
                    deficiency_data = []
                    labels = []
                    
                    if n_deficit_pct > 0:
                        deficiency_data.append(n_deficit_pct)
                        labels.append("Nitrogen (N)")
                    if p_deficit_pct > 0:
                        deficiency_data.append(p_deficit_pct)
                        labels.append("Phosphorus (P)")
                    if k_deficit_pct > 0:
                        deficiency_data.append(k_deficit_pct)
                        labels.append("Potassium (K)")
                    
                    if deficiency_data:
                        fig = px.pie(
                            values=deficiency_data,
                            names=labels,
                            title="Nutrient Deficiency Distribution",
                            color_discrete_sequence=px.colors.sequential.Viridis
                        )
                        st.plotly_chart(fig)
                    else:
                        st.info("Your soil has adequate nutrient levels. No significant deficiencies detected.")
                else:
                    st.info("Your soil has adequate nutrient levels. No significant deficiencies detected.")
                    
            # Generate PDF Report Section
            st.header("PDF Report")
            st.write("Get a comprehensive PDF report of your crop and fertilizer recommendations for offline reference.")
            
            # Collect all data for the PDF report
            field_conditions = {
                'soil_type': soil_type,
                'n_value': n_value,
                'p_value': p_value,
                'k_value': k_value,
                'temperature': temperature,
                'humidity': humidity,
                'ph_value': ph_value,
                'rainfall': rainfall
            }
            
            # Soil analysis for PDF
            soil_analysis = {
                'n_value': n_value,
                'p_value': p_value,
                'k_value': k_value
            }
            
            # Create PDF generation button
            pdf_col1, pdf_col2 = st.columns([2, 3])
            
            with pdf_col1:
                generate_pdf = st.button("Generate PDF Report")
                
            # Generate PDF when button is clicked
            if generate_pdf:
                with st.spinner("Generating PDF Report..."):
                    # Create the PDF report
                    b64_pdf, pdf_bytes = create_pdf_report(
                        field_conditions=field_conditions,
                        top_crops=top_crops,
                        top_probs=top_probs,
                        fertilizer_recs=fertilizer_recs,
                        soil_analysis=soil_analysis,
                        optimal_levels=optimal_levels,
                        crop_info=crop_info
                    )
                    
                    st.success("PDF Report Generated! You can now download or email it.")
                    
                    # Create columns for download and email buttons
                    download_col, email_col = st.columns(2)
                    
                    # Download button
                    with download_col:
                        st.download_button(
                            label="Download PDF Report",
                            data=pdf_bytes,
                            file_name="crop_fertilizer_report.pdf",
                            mime="application/pdf",
                            key='pdf-download'
                        )
                    
                    # Email section
                    with email_col:
                        # Add email input
                        email_address = st.text_input("Email address to send the report to:", placeholder="your.email@example.com")
                        
                        # Email button
                        if st.button("Email PDF Report"):
                            if email_address and "@" in email_address:
                                # Here we'll add the email sending logic
                                with st.spinner("Sending email..."):
                                    try:
                                        import smtplib
                                        from email.mime.multipart import MIMEMultipart
                                        from email.mime.base import MIMEBase
                                        from email.mime.text import MIMEText
                                        from email.utils import formatdate
                                        from email import encoders
                                        
                                        # Check if we have environment variables for email
                                        import os
                                        
                                        # Ask for email credentials if not already set
                                        if not os.environ.get('EMAIL_PASSWORD'):
                                            st.error("Email configuration required. Please ask the administrator to set up email credentials.")
                                        else:
                                            # Setup email
                                            sender_email = os.environ.get('EMAIL_USER', 'cropadviser@example.com')
                                            sender_password = os.environ.get('EMAIL_PASSWORD')
                                            
                                            msg = MIMEMultipart()
                                            msg['From'] = sender_email
                                            msg['To'] = email_address
                                            msg['Date'] = formatdate(localtime=True)
                                            msg['Subject'] = "Your Crop & Fertilizer Recommendation Report"
                                            
                                            # Email body
                                            email_body = f"""
                                            Hello,
                                            
                                            Thank you for using our Crop & Fertilizer Recommendation System.
                                            
                                            Attached is your personalized report based on the field conditions you provided.
                                            
                                            Top recommended crop: {top_crops[0] if top_crops else 'N/A'}
                                            
                                            This report includes detailed recommendations for crops, fertilizers, and soil analysis
                                            to help optimize your agricultural practices.
                                            
                                            Regards,
                                            Crop & Fertilizer Recommendation System
                                            """
                                            
                                            msg.attach(MIMEText(email_body))
                                            
                                            # Attach PDF
                                            part = MIMEBase('application', 'pdf')
                                            part.set_payload(pdf_bytes)
                                            encoders.encode_base64(part)
                                            part.add_header('Content-Disposition', 'attachment', filename="crop_fertilizer_report.pdf")
                                            msg.attach(part)
                                            
                                            # Connect to server and send email
                                            smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
                                            smtp_port = int(os.environ.get('SMTP_PORT', 587))
                                            
                                            with smtplib.SMTP(smtp_server, smtp_port) as server:
                                                server.starttls()
                                                server.login(sender_email, sender_password)
                                                server.sendmail(sender_email, email_address, msg.as_string())
                                            
                                            st.success(f"Email sent successfully to {email_address}!")
                                    except Exception as e:
                                        st.error(f"Failed to send email: {str(e)}")
                                        st.info("For testing purposes, you can use the download option instead.")
                            else:
                                st.error("Please enter a valid email address.")
        
# Settings page
elif page == "Settings":
    settings_page()

# Display educational information when on Home page but no form submitted
if page == "Home" and not submit_button:
    st.header("How it works")
    st.write("""
    1. Enter your field's environmental conditions in the sidebar
    2. Our system analyzes these conditions using a machine learning model
    3. You'll receive personalized crop recommendations with confidence scores
    4. Get fertilizer recommendations based on soil nutrient levels and selected crops
    5. Review detailed information and visualizations for optimal agricultural decisions
    6. Download a comprehensive PDF report for offline reference or sharing
    
    The model considers factors like soil nutrients (N, P, K), temperature, humidity, pH, and rainfall
    to determine which crops would thrive in your specific conditions and what fertilizers would 
    optimize your soil health and crop yield.
    """)
    
    # Show sample crops and their general requirements
    st.header("Sample Crop Requirements")
    
    # Create a sample dataframe for display
    sample_data = pd.DataFrame([
        ["Rice", "20-30°C", "5.5-6.5", "High (150-300 mm)"],
        ["Wheat", "15-25°C", "6.0-7.0", "Moderate (75-100 mm)"],
        ["Maize", "20-30°C", "5.5-7.0", "Moderate (80-110 mm)"],
        ["Potato", "15-20°C", "5.0-6.5", "Moderate (50-75 mm)"],
        ["Cotton", "20-30°C", "6.0-7.5", "Low to Moderate (60-100 mm)"]
    ], columns=["Crop", "Temperature", "pH Range", "Water Requirement"])
    
    st.table(sample_data)
    
    # Show sample fertilizer information
    st.header("Common Fertilizers")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("NPK Fertilizers")
        st.write("""
        NPK fertilizers contain three primary nutrients:
        - **Nitrogen (N)**: Promotes leaf growth and greening
        - **Phosphorus (P)**: Enhances root and flower development 
        - **Potassium (K)**: Improves overall plant health and disease resistance
        
        Common NPK formulations include 17-17-17 (balanced), 10-26-26 (root development), 
        and 14-35-14 (flowering enhancement).
        """)
    
    with col2:
        st.subheader("Single-Nutrient Fertilizers")
        st.write("""
        These fertilizers focus on a specific nutrient deficiency:
        - **Urea**: High nitrogen (46%) for leaf development
        - **DAP**: High phosphorus (46%) with some nitrogen (18%)
        - **MOP**: High potassium (60-62%) for fruit development
        - **SSP**: Provides phosphorus (16%) along with sulfur and calcium
        """)
    
    st.info("""
    **Tip:** The more accurate your input values, the better the recommendations will be.
    Consider getting your soil tested for precise nutrient levels and pH values.
    """)
