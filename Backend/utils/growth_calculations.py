from datetime import date
from typing import Dict, Literal, Optional

# WHO Growth Standards (0-24 months)
# Data structure: {age_in_days: {percentile: value}}
WHO_WEIGHT_FOR_AGE_BOYS = {
    # Format: age_in_days: {percentile: weight_kg}
    0: {3: 2.5, 15: 2.9, 50: 3.3, 85: 3.9, 97: 4.3},
    30: {3: 3.4, 15: 3.9, 50: 4.5, 85: 5.1, 97: 5.7},
    # Add more data points for each month up to 24 months
    365: {3: 7.8, 15: 8.5, 50: 9.6, 85: 10.8, 97: 11.8},
    730: {3: 9.6, 15: 10.2, 50: 11.5, 85: 12.9, 97: 14.1}
}

WHO_HEIGHT_FOR_AGE_BOYS = {
    # Format: age_in_days: {percentile: height_cm}
    0: {3: 46.1, 15: 47.5, 50: 49.9, 85: 51.8, 97: 53.4},
    30: {3: 50.8, 15: 52.3, 50: 54.7, 85: 56.7, 97: 58.4},
    # Add more data points for each month up to 24 months
    365: {3: 71.0, 15: 72.8, 50: 75.7, 85: 78.6, 97: 81.2},
    730: {3: 80.1, 15: 82.5, 50: 86.5, 85: 90.1, 97: 93.2}
}

WHO_WEIGHT_FOR_AGE_GIRLS = {
    # Similar structure for girls
    0: {3: 2.4, 15: 2.8, 50: 3.2, 85: 3.7, 97: 4.2},
    365: {3: 7.2, 15: 7.9, 50: 8.9, 85: 10.1, 97: 11.1},
    730: {3: 9.0, 15: 9.7, 50: 10.8, 85: 12.2, 97: 13.4}
}

WHO_HEIGHT_FOR_AGE_GIRLS = {
    # Similar structure for girls
    0: {3: 45.4, 15: 46.9, 50: 49.1, 85: 51.0, 97: 52.7},
    365: {3: 69.0, 15: 70.9, 50: 74.0, 85: 77.1, 97: 79.9},
    730: {3: 78.6, 15: 81.0, 50: 85.1, 85: 88.9, 97: 91.9}
}

def interpolate_percentile(age_days: int, value: float, growth_standards: Dict[int, Dict[int, float]]) -> float:
    """
    Interpolate percentile based on WHO growth standards.
    
    Args:
        age_days: Baby's age in days
        value: The measurement value (weight or height)
        growth_standards: The appropriate WHO growth standards dictionary
        
    Returns:
        Calculated percentile (0-100)
    """
    # Find the closest age brackets
    ages = sorted(growth_standards.keys())
    lower_age = max(a for a in ages if a <= age_days)
    upper_age = min(a for a in ages if a >= age_days)
    
    if lower_age == upper_age:
        standards = growth_standards[lower_age]
    else:
        # Interpolate between age brackets
        lower_standards = growth_standards[lower_age]
        upper_standards = growth_standards[upper_age]
        standards = {}
        for p in [3, 15, 50, 85, 97]:
            lower_val = lower_standards[p]
            upper_val = upper_standards[p]
            ratio = (age_days - lower_age) / (upper_age - lower_age)
            standards[p] = lower_val + (upper_val - lower_val) * ratio
    
    # Find where the value fits in the percentiles
    if value <= standards[3]:
        # Below 3rd percentile
        return 3 * (value / standards[3])
    elif value <= standards[15]:
        # Between 3rd and 15th
        return 3 + 12 * ((value - standards[3]) / (standards[15] - standards[3]))
    elif value <= standards[50]:
        # Between 15th and 50th
        return 15 + 35 * ((value - standards[15]) / (standards[50] - standards[15]))
    elif value <= standards[85]:
        # Between 50th and 85th
        return 50 + 35 * ((value - standards[50]) / (standards[85] - standards[50]))
    elif value <= standards[97]:
        # Between 85th and 97th
        return 85 + 12 * ((value - standards[85]) / (standards[97] - standards[85]))
    else:
        # Above 97th percentile
        return 97 + 3 * ((value - standards[97]) / (standards[97] * 0.1))  # Extrapolate

def calculate_weight_percentile(gender: Literal["male", "female"], age_days: int, weight_kg: float) -> float:
    """
    Calculate weight-for-age percentile based on WHO standards.
    
    Args:
        gender: "male" or "female"
        age_days: Baby's age in days (0-730)
        weight_kg: Baby's weight in kilograms
        
    Returns:
        Percentile (0-100)
    """
    standards = WHO_WEIGHT_FOR_AGE_BOYS if gender == "male" else WHO_WEIGHT_FOR_AGE_GIRLS
    return interpolate_percentile(age_days, weight_kg, standards)

def calculate_height_percentile(gender: Literal["male", "female"], age_days: int, height_cm: float) -> float:
    """
    Calculate height-for-age percentile based on WHO standards.
    
    Args:
        gender: "male" or "female"
        age_days: Baby's age in days (0-730)
        height_cm: Baby's height in centimeters
        
    Returns:
        Percentile (0-100)
    """
    standards = WHO_HEIGHT_FOR_AGE_BOYS if gender == "male" else WHO_HEIGHT_FOR_AGE_GIRLS
    return interpolate_percentile(age_days, height_cm, standards)

def determine_weight_status(weight_percentile: float) -> str:
    """
    Determine baby's weight status based on percentile.
    
    Args:
        weight_percentile: Calculated weight-for-age percentile (0-100)
        
    Returns:
        One of: "severely_underweight", "underweight", "normal", "overweight", "obese"
    """
    if weight_percentile < 3:
        return "severely_underweight"
    elif weight_percentile < 15:
        return "underweight"
    elif weight_percentile < 85:
        return "normal"
    elif weight_percentile < 97:
        return "overweight"
    else:
        return "obese"

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """
    Calculate BMI (kg/m²) for children over 2 years.
    
    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
        
    Returns:
        BMI value
    """
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)

def get_growth_assessment(
    gender: Literal["male", "female"],
    birth_date: date,
    measurement_date: date,
    weight_kg: float,
    height_cm: float
) -> Dict[str, float]:
    """
    Comprehensive growth assessment for a baby.
    
    Args:
        gender: "male" or "female"
        birth_date: Baby's birth date
        measurement_date: Date of measurement
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
        
    Returns:
        Dictionary with all growth metrics and assessment
    """
    age_days = (measurement_date - birth_date).days
    
    weight_percentile = calculate_weight_percentile(gender, age_days, weight_kg)
    height_percentile = calculate_height_percentile(gender, age_days, height_cm)
    weight_status = determine_weight_status(weight_percentile)
    
    # For babies over 2 years, calculate BMI
    bmi = None
    bmi_percentile = None
    if age_days > 730:  # Over 2 years
        bmi = calculate_bmi(weight_kg, height_cm)
        # BMI percentile calculation would require additional standards data
    
    return {
        "weight_percentile": round(weight_percentile, 1),
        "height_percentile": round(height_percentile, 1),
        "weight_status": weight_status,
        "bmi": round(bmi, 1) if bmi else None,
        "bmi_percentile": round(bmi_percentile, 1) if bmi_percentile else None,
    }