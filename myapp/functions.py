from decimal import Decimal
from .models import UnitConversion
import requests
from datetime import datetime

def convert_quantity(quantity, from_unit_code, to_unit_code):
    # Convert quantity to Decimal if it's not already
    if not isinstance(quantity, Decimal):
        quantity = Decimal(quantity)
    
    # If from_unit_code is equal to to_unit_code, no conversion needed
    if from_unit_code == to_unit_code or from_unit_code == 'OPS':
        return float(quantity)
    # Retrieve the conversion rate from the database
    try:
        conversion = UnitConversion.objects.get(FromCode=from_unit_code, ToCode=to_unit_code)
    except UnitConversion.DoesNotExist:
        raise ValueError("Conversion rate not found for provided units")

    # Calculate the converted quantity
    converted_quantity = float(quantity * Decimal(conversion.Value))

    return converted_quantity



def get_initials_with_dots(provider_name):
    # Split the name into individual words
    words = provider_name.split()

    # Initialize an empty list to store the initials
    initials_list = []

    # Iterate over each word and get its initial
    for word in words:
        # Get the first character of the word and capitalize it
        initial = word[0].upper()
        # Add the initial to the list
        initials_list.append(initial)

    # Join the initials with dots
    initials_with_dots = '.'.join(initials_list)

    return initials_with_dots

def geocode_location(location_name, api_key):
    url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{location_name}.json'
    params = {'access_token': api_key}
    response = requests.get(url, params=params)
    data = response.json()
    if 'features' in data and data['features']:
        # Extract coordinates from the first result
        coordinates = data['features'][0]['geometry']['coordinates']
        return coordinates
    else:
        return None
    
def from_unitcode_to_unitname(unitCode):
    # Implement the logic to map unit codes to unit names
    unit_mapping = {
        'LT': 'Litre',
        'M3': 'Cubic meter',
        'KG': 'KILOGRAMME',
        'T' : 'TONNE',
        'BL': 'Baril',
        'USG': 'USGallon',
        'HL': 'HECTOLITRE',

        # Add more mappings as needed
    }
    return unit_mapping.get(unitCode, unitCode)

from datetime import timedelta

def generate_textual_interpretation(data, start_date, end_date, time_increment, unit_code):
    total_consumption = sum(data)
    average_consumption_per_day = total_consumption / len(data)
    
    # Calculate percentage change
    if data[0] != 0:
        percentage_change = ((data[-1] - data[0]) / data[0]) * 100
    else:
        percentage_change = 0
    
    # Determine trend based on percentage change
    if percentage_change > 0:
        trend = "increasing"
    elif percentage_change < 0:
        trend = "decreasing"
    else:
        trend = "stable"
    
    # Extract the days component from the time increment
    time_increment_days = time_increment.days
    
    # Map time increments to corresponding time units
    time_units = {
        1: "day",
        7: "week",
        30: "month",
        90: "quarter",
        180: "half-year",
        365: "year"
    }
    
    # Determine the appropriate time unit
    if time_increment_days in time_units:
        time_unit = time_units[time_increment_days]
    else:
        time_unit = "time period"
    
    # Define insights based on the findings
    if total_consumption > 0:
        if percentage_change > 10:
            insight = f"There has been a significant increase in consumption compared to the start of the {time_unit}."
        elif percentage_change < -10:
            insight = f"There has been a significant decrease in consumption compared to the start of the {time_unit}."
        else:
            insight = f"Consumption levels have remained relatively stable over the {time_unit}."
    else:
        insight = f"There is no consumption data available for the given {time_unit}."
    
    # Provide suggestions for action or further analysis
    if time_increment_days <= 7:
        suggestion = "Consider analyzing daily consumption trends for more granular insights."
    elif time_increment_days <= 30:
        suggestion = "Explore weekly consumption patterns to identify longer-term trends and seasonality."
    else:
        suggestion = "Investigate monthly consumption trends for broader insights and planning."
    
    # Construct the interpretation message
    interpretation = (
        f"The total consumption over the {time_unit} is {total_consumption} {unit_code}. "
        f"The average consumption per {time_unit} is {average_consumption_per_day:.2f} {unit_code}. "
        f"The percentage change in consumption over the entire {time_unit} is {percentage_change:.2f}%. "
        f"The trend appears to be {trend}. "
        f"{insight} "
        f"The time increment of {time_increment_days} days helps identify short-term fluctuations and trends. "
        f"{suggestion}"
    )
    
    return interpretation
