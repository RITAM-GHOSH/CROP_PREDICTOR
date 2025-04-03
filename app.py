import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from crop_recommendation_model import train_model, predict_crop
from crop_data import crop_info, get_dataset

# Set page configuration
st.set_page_config(
    page_title="Crop Recommendation System",
    page_icon="🌱",
    layout="wide"
)

# App title and description
st.title("🌱 Crop Recommendation System")
st.write("""
This application helps farmers determine the optimal crops to plant based on their local environmental conditions.
Enter your field's characteristics below to receive personalized crop recommendations.
""")

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
if submit_button:
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
        
# Display educational information when no prediction is made yet
if not submit_button:
    st.header("How it works")
    st.write("""
    1. Enter your field's environmental conditions in the sidebar
    2. Our system analyzes these conditions using a machine learning model
    3. You'll receive personalized crop recommendations with confidence scores
    4. Review detailed information about each recommended crop
    
    The model considers factors like soil nutrients (N, P, K), temperature, humidity, pH, and rainfall
    to determine which crops would thrive in your specific conditions.
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
    
    st.info("""
    **Tip:** The more accurate your input values, the better the recommendations will be.
    Consider getting your soil tested for precise nutrient levels and pH values.
    """)
