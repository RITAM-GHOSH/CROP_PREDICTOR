import io
import base64
from fpdf import FPDF
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

class ReportPDF(FPDF):
    def header(self):
        # Add logo if needed
        # self.image('logo.png', 10, 8, 33)
        
        # Set font for header
        self.set_font('Arial', 'B', 14)
        
        # Add title
        self.cell(0, 10, 'Crop & Fertilizer Recommendation Report', 0, 1, 'C')
        
        # Add date
        self.set_font('Arial', 'I', 10)
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cell(0, 10, f'Generated on: {current_date}', 0, 1, 'R')
        
        # Add line break
        self.ln(5)

    def footer(self):
        # Set position at 1.5 cm from bottom
        self.set_y(-15)
        
        # Set font for footer
        self.set_font('Arial', 'I', 8)
        
        # Add page number
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

def create_pdf_report(field_conditions, top_crops, top_probs, fertilizer_recs, 
                      soil_analysis, optimal_levels, crop_info):
    """
    Generate a PDF report with the crop and fertilizer recommendations.
    
    Args:
        field_conditions: Dictionary with field input values
        top_crops: List of recommended crops
        top_probs: List of confidence scores for top crops
        fertilizer_recs: List of fertilizer recommendations
        soil_analysis: Dictionary with soil nutrient analysis
        optimal_levels: Dictionary with optimal nutrient levels
        crop_info: Dictionary with crop information
        
    Returns:
        base64 encoded PDF for download
    """
    # Create PDF object
    pdf = ReportPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Set font for main content
    pdf.set_font('Arial', '', 11)
    
    # Field Conditions Section
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Field Conditions', 0, 1, 'L')
    pdf.set_font('Arial', '', 11)
    
    # Format the field conditions as a table
    field_data = [
        ['Parameter', 'Value'],
        ['Soil Type', field_conditions['soil_type']],
        ['Nitrogen (N)', f"{field_conditions['n_value']} kg/ha"],
        ['Phosphorus (P)', f"{field_conditions['p_value']} kg/ha"],
        ['Potassium (K)', f"{field_conditions['k_value']} kg/ha"],
        ['Temperature', f"{field_conditions['temperature']}°C"],
        ['Humidity', f"{field_conditions['humidity']}%"],
        ['pH Value', f"{field_conditions['ph_value']}"],
        ['Rainfall', f"{field_conditions['rainfall']} mm"]
    ]
    
    # Column widths for the field conditions table
    col_width = pdf.w / 2 - 15
    
    # Print field conditions table
    for i, row in enumerate(field_data):
        if i == 0:  # Header row
            pdf.set_font('Arial', 'B', 11)
        else:
            pdf.set_font('Arial', '', 11)
        
        pdf.cell(col_width, 8, row[0], 1, 0, 'L')
        pdf.cell(col_width, 8, str(row[1]), 1, 1, 'L')
    
    pdf.ln(5)
    
    # Crop Recommendations Section
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Recommended Crops', 0, 1, 'L')
    pdf.set_font('Arial', '', 11)
    
    # Create a table for crop recommendations
    for i, (crop, prob) in enumerate(zip(top_crops, top_probs)):
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 8, f"{i+1}. {crop} (Confidence: {prob:.1f}%)", 0, 1, 'L')
        pdf.set_font('Arial', '', 11)
        
        if crop in crop_info:
            info = crop_info[crop]
            pdf.cell(0, 8, f"Description: {info['description']}", 0, 1, 'L')
            pdf.cell(0, 8, f"Growing Season: {info['growing_season']}", 0, 1, 'L')
            pdf.cell(0, 8, "Ideal Conditions:", 0, 1, 'L')
            pdf.cell(0, 8, f"- Temperature: {info['ideal_temp']}", 0, 1, 'L')
            pdf.cell(0, 8, f"- Soil pH: {info['ideal_ph']}", 0, 1, 'L')
            pdf.cell(0, 8, f"- Water Needs: {info['water_needs']}", 0, 1, 'L')
        
        pdf.ln(3)
    
    pdf.ln(5)
    
    # Fertilizer Recommendations Section
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Fertilizer Recommendations', 0, 1, 'L')
    pdf.set_font('Arial', '', 11)
    
    for i, rec in enumerate(fertilizer_recs):
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 8, f"{i+1}. {rec['fertilizer']}", 0, 1, 'L')
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(0, 8, f"Rationale: {rec['rationale']}", 0, 'L')
        pdf.ln(3)
    
    pdf.ln(5)
    
    # Soil Analysis Section
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Soil Nutrient Analysis', 0, 1, 'L')
    pdf.set_font('Arial', '', 11)
    
    # Create a table for soil nutrient analysis
    nutrient_table = [
        ['Nutrient', 'Current Level', 'Optimal Level', 'Status'],
        ['Nitrogen (N)', f"{soil_analysis['n_value']} kg/ha", f"{optimal_levels['N']} kg/ha", 
         'Deficient' if soil_analysis['n_value'] < optimal_levels['N'] else 'Adequate'],
        ['Phosphorus (P)', f"{soil_analysis['p_value']} kg/ha", f"{optimal_levels['P']} kg/ha",
         'Deficient' if soil_analysis['p_value'] < optimal_levels['P'] else 'Adequate'],
        ['Potassium (K)', f"{soil_analysis['k_value']} kg/ha", f"{optimal_levels['K']} kg/ha",
         'Deficient' if soil_analysis['k_value'] < optimal_levels['K'] else 'Adequate']
    ]
    
    # Column widths for the nutrient analysis table
    col_width = pdf.w / 4 - 8
    
    # Print nutrient analysis table
    for i, row in enumerate(nutrient_table):
        if i == 0:  # Header row
            pdf.set_font('Arial', 'B', 11)
        else:
            pdf.set_font('Arial', '', 11)
        
        for j, cell in enumerate(row):
            if j == 3 and i > 0:  # Status column
                # Set fill color based on status
                if cell == 'Deficient':
                    pdf.set_text_color(194, 59, 34)  # Red for deficient
                else:
                    pdf.set_text_color(52, 168, 83)  # Green for adequate
            
            pdf.cell(col_width, 8, str(cell), 1, 0, 'L')
            pdf.set_text_color(0, 0, 0)  # Reset text color
        
        pdf.ln()
    
    pdf.ln(5)
    
    # Summary Section
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Summary and Recommendations', 0, 1, 'L')
    pdf.set_font('Arial', '', 11)
    
    # Most recommended crop
    top_crop = top_crops[0] if top_crops else "None"
    top_prob = top_probs[0] if top_probs else 0
    
    summary_text = f"Based on your field conditions, we recommend {top_crop} as the optimal crop "
    summary_text += f"with a confidence of {top_prob:.1f}%. "
    
    # Add fertilizer summary
    if fertilizer_recs:
        summary_text += f"To optimize growth, we recommend using {fertilizer_recs[0]['fertilizer']} "
        summary_text += f"as the primary fertilizer. {fertilizer_recs[0]['rationale']}"
    
    pdf.multi_cell(0, 8, summary_text, 0, 'L')
    
    pdf.ln(5)
    
    # Final tips
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, "Additional Tips:", 0, 1, 'L')
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 8, "• Consider soil testing regularly to monitor nutrient levels.", 0, 'L')
    pdf.multi_cell(0, 8, "• Apply fertilizers according to recommended rates and timing.", 0, 'L')
    pdf.multi_cell(0, 8, "• Monitor water requirements throughout the growing season.", 0, 'L')
    pdf.multi_cell(0, 8, "• Rotate crops to maintain soil health and prevent pest buildup.", 0, 'L')
    
    # Save the PDF to a bytes buffer
    pdf_output = io.BytesIO()
    
    # The output method returns a bytearray in newer versions of fpdf
    pdf_data = pdf.output(dest='S')
    
    # If the output is a string (older fpdf versions), encode it to bytes
    if isinstance(pdf_data, str):
        pdf_data = pdf_data.encode('latin1')
    
    # Write to BytesIO
    pdf_output.write(pdf_data)
    pdf_output.seek(0)
    
    # Encode PDF to base64 for download
    b64_pdf = base64.b64encode(pdf_output.read()).decode('utf-8')
    
    return b64_pdf

def get_download_link(b64_pdf, filename="crop_fertilizer_report.pdf"):
    """
    Generate a download link for the PDF report.
    
    Args:
        b64_pdf: Base64 encoded PDF
        filename: Filename for download
        
    Returns:
        HTML download link
    """
    # Create a Streamlit download button for more reliability than raw HTML
    import streamlit as st
    
    # Convert base64 to bytes for download button
    pdf_bytes = base64.b64decode(b64_pdf)
    
    # Use Streamlit's download button
    return st.download_button(
        label="Download PDF Report",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf"
    )