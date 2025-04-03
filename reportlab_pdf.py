import io
import base64
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch
from datetime import datetime

def create_pdf_report(field_conditions, top_crops, top_probs, fertilizer_recs, 
                      soil_analysis, optimal_levels, crop_info):
    """
    Generate a PDF report with crop and fertilizer recommendations using ReportLab.
    
    Returns:
        bytes: PDF file as bytes
    """
    # Create a file-like buffer to receive PDF data
    buffer = io.BytesIO()
    
    # Create the PDF object using the buffer as its "file"
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Initialize story with flowable elements
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    heading2_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Custom styles
    subtitle_style = ParagraphStyle(
        'subtitle',
        parent=styles['Heading2'],
        textColor=colors.darkblue,
        spaceAfter=12
    )
    
    info_style = ParagraphStyle(
        'info',
        parent=styles['Normal'],
        fontSize=10,
        leftIndent=20
    )
    
    # Title
    story.append(Paragraph("Crop & Fertilizer Recommendation Report", title_style))
    
    # Date
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    story.append(Paragraph(f"Generated on: {current_date}", styles['Italic']))
    story.append(Spacer(1, 0.2*inch))
    
    # Field Conditions Section
    story.append(Paragraph("Field Conditions", subtitle_style))
    
    # Create field conditions table
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
    
    field_table = Table(field_data, colWidths=[2*inch, 3*inch])
    
    field_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.black),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (1, 0), 12),
        ('BACKGROUND', (0, 1), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(field_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Crop Recommendations Section
    story.append(Paragraph("Recommended Crops", subtitle_style))
    
    for i, (crop, prob) in enumerate(zip(top_crops, top_probs)):
        story.append(Paragraph(f"{i+1}. {crop} (Confidence: {prob:.1f}%)", heading2_style))
        
        if crop in crop_info:
            info = crop_info[crop]
            story.append(Paragraph(f"<b>Description:</b> {info['description']}", info_style))
            story.append(Paragraph(f"<b>Growing Season:</b> {info['growing_season']}", info_style))
            story.append(Paragraph(f"<b>Ideal Conditions:</b>", info_style))
            story.append(Paragraph(f"- Temperature: {info['ideal_temp']}", info_style))
            story.append(Paragraph(f"- Soil pH: {info['ideal_ph']}", info_style))
            story.append(Paragraph(f"- Water Needs: {info['water_needs']}", info_style))
        
        story.append(Spacer(1, 0.1*inch))
    
    story.append(Spacer(1, 0.1*inch))
    
    # Fertilizer Recommendations Section
    story.append(Paragraph("Fertilizer Recommendations", subtitle_style))
    
    for i, rec in enumerate(fertilizer_recs):
        story.append(Paragraph(f"{i+1}. {rec['fertilizer']}", heading2_style))
        story.append(Paragraph(f"<b>Rationale:</b> {rec['rationale']}", info_style))
        story.append(Spacer(1, 0.1*inch))
    
    story.append(Spacer(1, 0.1*inch))
    
    # Soil Analysis Section
    story.append(Paragraph("Soil Nutrient Analysis", subtitle_style))
    
    # Create nutrient analysis table
    nutrient_data = [
        ['Nutrient', 'Current Level', 'Optimal Level', 'Status'],
    ]
    
    # Add N, P, K data
    for nutrient, label in [('n_value', 'Nitrogen (N)'), ('p_value', 'Phosphorus (P)'), ('k_value', 'Potassium (K)')]:
        optimal = optimal_levels['N' if nutrient == 'n_value' else 'P' if nutrient == 'p_value' else 'K']
        status = 'Deficient' if soil_analysis[nutrient] < optimal else 'Adequate'
        nutrient_data.append([
            label,
            f"{soil_analysis[nutrient]} kg/ha",
            f"{optimal} kg/ha", 
            status
        ])
    
    nutrient_table = Table(nutrient_data, colWidths=[1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
    
    nutrient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (3, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (3, 0), colors.black),
        ('ALIGN', (0, 0), (3, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (3, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (3, 0), 12),
        ('BOTTOMPADDING', (0, 0), (3, 0), 12),
        ('BACKGROUND', (0, 1), (3, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        # Color the status cell based on value
        ('TEXTCOLOR', (3, 1), (3, 1), colors.red if nutrient_data[1][3] == 'Deficient' else colors.green),
        ('TEXTCOLOR', (3, 2), (3, 2), colors.red if nutrient_data[2][3] == 'Deficient' else colors.green),
        ('TEXTCOLOR', (3, 3), (3, 3), colors.red if nutrient_data[3][3] == 'Deficient' else colors.green),
    ]))
    
    story.append(nutrient_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Summary Section
    story.append(Paragraph("Summary and Recommendations", subtitle_style))
    
    # Most recommended crop
    top_crop = top_crops[0] if top_crops else "None"
    top_prob = top_probs[0] if top_probs else 0
    
    summary_text = f"Based on your field conditions, we recommend <b>{top_crop}</b> as the optimal crop "
    summary_text += f"with a confidence of {top_prob:.1f}%. "
    
    # Add fertilizer summary
    if fertilizer_recs:
        summary_text += f"To optimize growth, we recommend using <b>{fertilizer_recs[0]['fertilizer']}</b> "
        summary_text += f"as the primary fertilizer. {fertilizer_recs[0]['rationale']}"
    
    story.append(Paragraph(summary_text, normal_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Final tips
    story.append(Paragraph("Additional Tips:", heading2_style))
    story.append(Paragraph("• Consider soil testing regularly to monitor nutrient levels.", normal_style))
    story.append(Paragraph("• Apply fertilizers according to recommended rates and timing.", normal_style))
    story.append(Paragraph("• Monitor water requirements throughout the growing season.", normal_style))
    story.append(Paragraph("• Rotate crops to maintain soil health and prevent pest buildup.", normal_style))
    
    # Build the PDF
    doc.build(story)
    
    # Get the value of the BytesIO buffer
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    # Encode in base64
    b64_pdf = base64.b64encode(pdf_bytes).decode()
    
    return b64_pdf, pdf_bytes