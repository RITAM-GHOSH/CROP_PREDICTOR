import pandas as pd
import numpy as np

def get_dataset():
    """
    Creates a synthetic crop recommendation dataset based on agricultural knowledge.
    
    This is used as a fallback when no real dataset is provided.
    In a production environment, this should be replaced with a real dataset.
    
    Returns:
        pandas.DataFrame: Dataset for crop recommendations
    """
    # Create a synthetic dataset based on agricultural knowledge
    # This is a simplified approximation and should be replaced with real data
    
    # Define crops and their typical growing conditions
    crops = [
        # Crop, N, P, K, temperature, humidity, ph, rainfall
        ["rice", 80, 40, 40, 23, 80, 6.5, 200],
        ["rice", 85, 45, 45, 24, 85, 6.0, 210],
        ["rice", 90, 45, 40, 25, 82, 6.2, 205],
        ["maize", 85, 60, 55, 22, 60, 6.5, 85],
        ["maize", 80, 55, 50, 23, 65, 6.7, 90],
        ["maize", 90, 65, 60, 24, 62, 6.3, 88],
        ["wheat", 75, 50, 45, 18, 60, 6.8, 70],
        ["wheat", 70, 55, 40, 17, 65, 7.0, 65],
        ["wheat", 80, 45, 50, 19, 55, 6.5, 75],
        ["mungbean", 20, 60, 20, 30, 70, 6.5, 90],
        ["mungbean", 25, 65, 25, 31, 75, 6.7, 85],
        ["mungbean", 18, 55, 18, 29, 68, 6.3, 95],
        ["jute", 80, 40, 40, 32, 80, 6.8, 170],
        ["jute", 85, 45, 45, 33, 85, 7.0, 165],
        ["jute", 75, 35, 35, 31, 75, 6.5, 175],
        ["cotton", 115, 45, 40, 28, 70, 6.5, 90],
        ["cotton", 110, 50, 45, 29, 75, 6.8, 85],
        ["cotton", 120, 40, 35, 27, 65, 6.3, 95],
        ["coconut", 20, 10, 30, 27, 80, 6.0, 180],
        ["coconut", 25, 15, 35, 28, 85, 6.2, 185],
        ["coconut", 18, 8, 25, 26, 75, 5.8, 175],
        ["papaya", 100, 30, 30, 26, 75, 6.5, 150],
        ["papaya", 105, 35, 35, 27, 80, 6.7, 145],
        ["papaya", 95, 25, 25, 25, 70, 6.3, 155],
        ["orange", 40, 10, 40, 24, 70, 6.0, 140],
        ["orange", 45, 15, 45, 25, 75, 6.2, 135],
        ["orange", 35, 5, 35, 23, 65, 5.8, 145],
        ["apple", 40, 20, 40, 21, 70, 6.5, 110],
        ["apple", 45, 25, 45, 22, 75, 6.7, 105],
        ["apple", 35, 15, 35, 20, 65, 6.3, 115],
        ["muskmelon", 100, 50, 80, 27, 60, 6.5, 90],
        ["muskmelon", 105, 55, 85, 28, 65, 6.7, 85],
        ["muskmelon", 95, 45, 75, 26, 55, 6.3, 95],
        ["watermelon", 100, 50, 80, 28, 65, 6.5, 80],
        ["watermelon", 105, 55, 85, 29, 70, 6.7, 75],
        ["watermelon", 95, 45, 75, 27, 60, 6.3, 85],
        ["grapes", 20, 125, 200, 26, 80, 5.5, 80],
        ["grapes", 25, 130, 205, 27, 85, 5.7, 75],
        ["grapes", 15, 120, 195, 25, 75, 5.3, 85],
        ["banana", 100, 75, 50, 25, 75, 6.5, 100],
        ["banana", 105, 80, 55, 26, 80, 6.7, 95],
        ["banana", 95, 70, 45, 24, 70, 6.3, 105],
        ["mango", 20, 20, 30, 27, 60, 5.5, 110],
        ["mango", 25, 25, 35, 28, 65, 5.7, 105],
        ["mango", 15, 15, 25, 26, 55, 5.3, 115],
        ["pomegranate", 40, 40, 40, 28, 65, 5.5, 60],
        ["pomegranate", 45, 45, 45, 29, 70, 5.7, 55],
        ["pomegranate", 35, 35, 35, 27, 60, 5.3, 65],
        ["chickpea", 40, 60, 80, 24, 65, 6.8, 70],
        ["chickpea", 45, 65, 85, 25, 70, 7.0, 65],
        ["chickpea", 35, 55, 75, 23, 60, 6.5, 75],
        ["coffee", 100, 20, 30, 23, 80, 5.5, 150],
        ["coffee", 105, 25, 35, 24, 85, 5.7, 145],
        ["coffee", 95, 15, 25, 22, 75, 5.3, 155],
        ["lentil", 40, 60, 80, 23, 60, 6.5, 60],
        ["lentil", 45, 65, 85, 24, 65, 6.7, 55],
        ["lentil", 35, 55, 75, 22, 55, 6.3, 65],
        ["pigeonpeas", 20, 60, 40, 26, 70, 6.5, 90],
        ["pigeonpeas", 25, 65, 45, 27, 75, 6.7, 85],
        ["pigeonpeas", 15, 55, 35, 25, 65, 6.3, 95],
        ["mothbeans", 30, 30, 20, 28, 60, 6.5, 50],
        ["mothbeans", 35, 35, 25, 29, 65, 6.7, 45],
        ["mothbeans", 25, 25, 15, 27, 55, 6.3, 55],
        ["blackgram", 40, 60, 20, 25, 75, 6.8, 80],
        ["blackgram", 45, 65, 25, 26, 80, 7.0, 75],
        ["blackgram", 35, 55, 15, 24, 70, 6.5, 85]
    ]
    
    # Create variations by adding some noise to make the dataset more realistic
    np.random.seed(42)
    expanded_data = []
    
    for crop_data in crops:
        # Create 5 variations with some noise for each crop
        for _ in range(5):
            crop = crop_data[0]
            features = np.array(crop_data[1:])
            
            # Add random noise (within 5-10% of original values)
            noise_factors = 1 + np.random.uniform(-0.1, 0.1, size=features.shape)
            noisy_features = features * noise_factors
            
            # Round numerical values appropriately
            noisy_features = np.round(noisy_features, 1)
            
            expanded_data.append([crop] + noisy_features.tolist())
    
    # Create DataFrame
    columns = ['label', 'N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    df = pd.DataFrame(expanded_data, columns=columns)
    
    # Add a small amount of random samples to simulate outliers and edge cases
    return df

# Crop information dictionary
crop_info = {
    "rice": {
        "description": "A staple food crop for more than half the world's population.",
        "growing_season": "Typically grown in summer, requires 3-6 months to mature.",
        "ideal_temp": "20-27°C",
        "ideal_ph": "5.5-6.5",
        "water_needs": "High - requires standing water during most of its growth."
    },
    "maize": {
        "description": "Also known as corn, a versatile crop used for food, feed, and industrial products.",
        "growing_season": "Warm season crop, requires 90-120 days to mature.",
        "ideal_temp": "20-25°C",
        "ideal_ph": "5.8-7.0",
        "water_needs": "Moderate - requires consistent moisture throughout growing season."
    },
    "wheat": {
        "description": "One of the world's most important cereal grains, used primarily for bread and pasta.",
        "growing_season": "Winter or spring crop depending on variety, requires 4-8 months to mature.",
        "ideal_temp": "15-20°C",
        "ideal_ph": "6.0-7.0",
        "water_needs": "Moderate - sensitive to both drought and excessive moisture."
    },
    "mungbean": {
        "description": "A small, green bean used in Asian cuisine, salads, and sprouting.",
        "growing_season": "Warm season crop, requires 60-90 days to mature.",
        "ideal_temp": "28-30°C",
        "ideal_ph": "6.2-7.2",
        "water_needs": "Moderate - drought-tolerant once established."
    },
    "jute": {
        "description": "A fiber crop used primarily for making burlap, hessian, or gunny cloth.",
        "growing_season": "Warm season crop, requires 120-150 days to mature.",
        "ideal_temp": "25-35°C",
        "ideal_ph": "6.0-7.5",
        "water_needs": "High - requires consistent moisture throughout growing season."
    },
    "cotton": {
        "description": "A soft fiber that grows around the seeds of the cotton plant, a major textile crop.",
        "growing_season": "Warm season crop, requires 150-180 days to mature.",
        "ideal_temp": "25-30°C",
        "ideal_ph": "5.8-8.0",
        "water_needs": "Moderate - drought-tolerant once established but needs consistent moisture for best yields."
    },
    "coconut": {
        "description": "A tropical tree crop that produces fruits with a hard shell containing edible meat and liquid.",
        "growing_season": "Perennial crop that produces year-round after 6-10 years of planting.",
        "ideal_temp": "25-30°C",
        "ideal_ph": "5.5-7.0",
        "water_needs": "High - requires consistent moisture throughout the year."
    },
    "papaya": {
        "description": "A tropical fruit tree with sweet, orange flesh and black seeds.",
        "growing_season": "Perennial that begins fruiting within 10-12 months of planting.",
        "ideal_temp": "22-28°C",
        "ideal_ph": "6.0-7.0",
        "water_needs": "Moderate to high - sensitive to drought and waterlogging."
    },
    "orange": {
        "description": "A citrus fruit grown on trees, known for its sweet-tart flavor and high vitamin C content.",
        "growing_season": "Perennial that takes 7-8 months from flowering to harvest.",
        "ideal_temp": "15-29°C",
        "ideal_ph": "5.5-6.5",
        "water_needs": "Moderate - needs consistent moisture but good drainage."
    },
    "apple": {
        "description": "A popular deciduous tree fruit known for its crisp texture and various flavors.",
        "growing_season": "Perennial that blooms in spring and harvests in fall.",
        "ideal_temp": "15-24°C",
        "ideal_ph": "6.0-7.0",
        "water_needs": "Moderate - requires consistent moisture, especially during fruit development."
    },
    "muskmelon": {
        "description": "A sweet, aromatic fruit in the gourd family, related to cantaloupe.",
        "growing_season": "Warm season crop, requires 80-110 days to mature.",
        "ideal_temp": "24-32°C",
        "ideal_ph": "6.0-7.0",
        "water_needs": "Moderate - needs consistent moisture until fruit formation, then reduced."
    },
    "watermelon": {
        "description": "A large, sweet fruit with juicy red flesh and black seeds, popular in summer.",
        "growing_season": "Warm season crop, requires 80-110 days to mature.",
        "ideal_temp": "25-30°C",
        "ideal_ph": "6.0-7.0",
        "water_needs": "Moderate - needs consistent moisture until fruit formation, then reduced."
    },
    "grapes": {
        "description": "Perennial woody vines that produce clusters of berries used for wine, juice, and fresh consumption.",
        "growing_season": "Perennial that produces fruits in late summer to fall.",
        "ideal_temp": "15-30°C",
        "ideal_ph": "5.5-6.5",
        "water_needs": "Low to moderate - established vines can be relatively drought-tolerant."
    },
    "banana": {
        "description": "A tropical fruit that grows in hanging clusters on large herbaceous plants.",
        "growing_season": "Perennial that produces fruit year-round in tropical climates.",
        "ideal_temp": "22-31°C",
        "ideal_ph": "5.5-7.0",
        "water_needs": "High - requires consistent moisture throughout growing season."
    },
    "mango": {
        "description": "A juicy stone fruit from tropical trees, known for its sweet flavor and fibrous texture.",
        "growing_season": "Perennial that typically flowers in winter and fruits in summer.",
        "ideal_temp": "24-30°C",
        "ideal_ph": "5.5-7.5",
        "water_needs": "Moderate - established trees are somewhat drought-tolerant."
    },
    "pomegranate": {
        "description": "A fruit-bearing deciduous shrub with red, edible seeds called arils.",
        "growing_season": "Perennial that typically bears fruit 5-7 months after flowering.",
        "ideal_temp": "18-35°C",
        "ideal_ph": "5.5-7.0",
        "water_needs": "Low to moderate - quite drought-tolerant once established."
    },
    "chickpea": {
        "description": "A protein-rich legume used in various cuisines, also known as garbanzo beans.",
        "growing_season": "Cool season crop, requires 90-120 days to mature.",
        "ideal_temp": "18-26°C",
        "ideal_ph": "6.0-8.0",
        "water_needs": "Low to moderate - relatively drought-tolerant once established."
    },
    "coffee": {
        "description": "A perennial crop grown for its beans, which are roasted to make coffee beverages.",
        "growing_season": "Perennial that begins producing beans after 3-5 years.",
        "ideal_temp": "15-24°C",
        "ideal_ph": "5.0-6.0",
        "water_needs": "Moderate - needs consistent moisture but good drainage."
    },
    "lentil": {
        "description": "A small, lens-shaped legume high in protein and a dietary staple in many regions.",
        "growing_season": "Cool season crop, requires 80-110 days to mature.",
        "ideal_temp": "15-25°C",
        "ideal_ph": "6.0-8.0",
        "water_needs": "Low to moderate - relatively drought-tolerant."
    },
    "pigeonpeas": {
        "description": "A perennial legume grown for its edible seeds, also known as red gram or arhar dal.",
        "growing_season": "Warm season crop, requires 120-180 days to mature.",
        "ideal_temp": "20-30°C",
        "ideal_ph": "5.0-7.0",
        "water_needs": "Low - highly drought-tolerant once established."
    },
    "mothbeans": {
        "description": "A drought-resistant legume grown mainly in arid and semi-arid regions.",
        "growing_season": "Warm season crop, requires 75-90 days to mature.",
        "ideal_temp": "25-35°C",
        "ideal_ph": "6.0-7.0",
        "water_needs": "Very low - extremely drought-tolerant."
    },
    "blackgram": {
        "description": "A bean grown primarily in the Indian subcontinent, also known as urad dal.",
        "growing_season": "Warm season crop, requires 70-90 days to mature.",
        "ideal_temp": "25-35°C",
        "ideal_ph": "6.5-7.5",
        "water_needs": "Moderate - sensitive to both drought and excessive moisture."
    }
}

# Fertilizer information dictionary
fertilizer_info = {
    "NPK 10-26-26": {
        "description": "Balanced fertilizer with higher phosphorus and potassium content.",
        "ideal_for": ["wheat", "barley", "oats"],
        "n_content": "10%",
        "p_content": "26%",
        "k_content": "26%",
        "application_rate": "200-250 kg/ha",
        "best_time": "Pre-sowing or at sowing time"
    },
    "NPK 17-17-17": {
        "description": "Balanced all-purpose fertilizer with equal amounts of N, P, and K.",
        "ideal_for": ["maize", "cotton", "sugarcane"],
        "n_content": "17%",
        "p_content": "17%",
        "k_content": "17%",
        "application_rate": "250-300 kg/ha",
        "best_time": "At planting or early growth stage"
    },
    "Urea": {
        "description": "High nitrogen fertilizer ideal for leafy growth.",
        "ideal_for": ["rice", "maize", "wheat", "vegetables"],
        "n_content": "46%",
        "p_content": "0%",
        "k_content": "0%",
        "application_rate": "100-150 kg/ha",
        "best_time": "Multiple small applications during growing season"
    },
    "DAP (Diammonium Phosphate)": {
        "description": "High phosphorus fertilizer with some nitrogen.",
        "ideal_for": ["wheat", "rice", "vegetables", "fruits"],
        "n_content": "18%",
        "p_content": "46%",
        "k_content": "0%",
        "application_rate": "100-125 kg/ha",
        "best_time": "Pre-sowing or at sowing time"
    },
    "MOP (Muriate of Potash)": {
        "description": "High potassium fertilizer for fruit and root development.",
        "ideal_for": ["potatoes", "sugarcane", "fruits", "vegetables"],
        "n_content": "0%",
        "p_content": "0%",
        "k_content": "60-62%",
        "application_rate": "75-100 kg/ha",
        "best_time": "Pre-planting or during growth stage"
    },
    "SSP (Single Super Phosphate)": {
        "description": "Provides phosphorus, sulfur, and calcium. Good for legumes.",
        "ideal_for": ["pulses", "oilseeds", "millet"],
        "n_content": "0%",
        "p_content": "16%",
        "k_content": "0%",
        "application_rate": "200-250 kg/ha",
        "best_time": "Pre-sowing or at sowing time"
    },
    "Ammonium Sulfate": {
        "description": "Provides nitrogen and sulfur, good for sulfur-deficient soils.",
        "ideal_for": ["rice", "vegetables", "tea", "coffee"],
        "n_content": "21%",
        "p_content": "0%",
        "k_content": "0%",
        "application_rate": "100-150 kg/ha",
        "best_time": "Early to mid-growing season"
    },
    "NPK 14-35-14": {
        "description": "High phosphorus formula good for root development and flowering.",
        "ideal_for": ["vegetables", "fruits", "ornamentals"],
        "n_content": "14%",
        "p_content": "35%",
        "k_content": "14%",
        "application_rate": "200-250 kg/ha",
        "best_time": "At planting and pre-flowering stage"
    }
}

def recommend_fertilizer(n_value, p_value, k_value, crop=None):
    """
    Recommends appropriate fertilizers based on soil NPK values and optionally for a specific crop.
    
    Args:
        n_value: Nitrogen content in soil (kg/ha)
        p_value: Phosphorus content in soil (kg/ha)
        k_value: Potassium content in soil (kg/ha)
        crop: Optional - specific crop name for targeted recommendations
        
    Returns:
        list: List of recommended fertilizers with rationale
    """
    recommendations = []
    
    # Define optimal ranges for different crops or use general ranges
    optimal_n = 80
    optimal_p = 40
    optimal_k = 40
    
    # Adjust optimal values if crop is specified
    if crop:
        crop_lower = crop.lower()
        if crop_lower in ["rice", "maize", "wheat"]:
            optimal_n = 120
            optimal_p = 60
            optimal_k = 50
        elif crop_lower in ["vegetables", "tomato", "potato", "cabbage"]:
            optimal_n = 100
            optimal_p = 80
            optimal_k = 80
        elif crop_lower in ["fruits", "mango", "apple", "banana"]:
            optimal_n = 80
            optimal_p = 60
            optimal_k = 100
        elif crop_lower in ["pulses", "chickpea", "lentil", "beans"]:
            optimal_n = 40
            optimal_p = 60
            optimal_k = 40
    
    # Calculate deficiencies
    n_deficit = max(0, optimal_n - n_value)
    p_deficit = max(0, optimal_p - p_value)
    k_deficit = max(0, optimal_k - k_value)
    
    # Determine which nutrients are most deficient
    severe_n_deficiency = n_deficit > 30
    severe_p_deficiency = p_deficit > 20
    severe_k_deficiency = k_deficit > 20
    
    # Make recommendations based on deficiencies
    if severe_n_deficiency and not severe_p_deficiency and not severe_k_deficiency:
        recommendations.append({
            "fertilizer": "Urea",
            "rationale": f"Soil is primarily deficient in nitrogen (N deficit: {n_deficit} kg/ha). Urea provides high nitrogen content to promote leaf and stem growth."
        })
    
    elif severe_p_deficiency and not severe_n_deficiency and not severe_k_deficiency:
        recommendations.append({
            "fertilizer": "DAP (Diammonium Phosphate)",
            "rationale": f"Soil is primarily deficient in phosphorus (P deficit: {p_deficit} kg/ha). DAP provides high phosphorus content to promote root development and flowering."
        })
    
    elif severe_k_deficiency and not severe_n_deficiency and not severe_p_deficiency:
        recommendations.append({
            "fertilizer": "MOP (Muriate of Potash)",
            "rationale": f"Soil is primarily deficient in potassium (K deficit: {k_deficit} kg/ha). MOP provides high potassium content to promote fruit development and disease resistance."
        })
    
    elif severe_n_deficiency and severe_p_deficiency and severe_k_deficiency:
        recommendations.append({
            "fertilizer": "NPK 17-17-17",
            "rationale": f"Soil is deficient in all major nutrients (N: {n_deficit}, P: {p_deficit}, K: {k_deficit} kg/ha). A balanced NPK fertilizer will address all deficiencies."
        })
    
    elif severe_p_deficiency and severe_k_deficiency:
        recommendations.append({
            "fertilizer": "NPK 10-26-26",
            "rationale": f"Soil is deficient in phosphorus and potassium (P: {p_deficit}, K: {k_deficit} kg/ha). This fertilizer has higher P and K content to address these deficiencies."
        })
    
    elif severe_n_deficiency and severe_p_deficiency:
        recommendations.append({
            "fertilizer": "NPK 14-35-14",
            "rationale": f"Soil is deficient in nitrogen and phosphorus (N: {n_deficit}, P: {p_deficit} kg/ha). This fertilizer has balanced N and higher P content."
        })
    
    else:
        # If no severe deficiencies or special cases
        if n_deficit + p_deficit + k_deficit > 30:
            recommendations.append({
                "fertilizer": "NPK 17-17-17",
                "rationale": "Soil has moderate deficiencies across multiple nutrients. A balanced fertilizer will help maintain overall soil fertility."
            })
        else:
            recommendations.append({
                "fertilizer": "Organic Compost",
                "rationale": "Soil nutrient levels are relatively adequate. Organic compost is recommended for sustainable soil health improvement."
            })
    
    # Add a second recommendation if applicable
    if crop and len(recommendations) < 2:
        for fert_name, fert_data in fertilizer_info.items():
            if crop.lower() in fert_data["ideal_for"] and fert_name != recommendations[0]["fertilizer"]:
                recommendations.append({
                    "fertilizer": fert_name,
                    "rationale": f"Specifically recommended for {crop} cultivation based on typical crop requirements."
                })
                break
    
    return recommendations
