# data_collection.py (in habessinica/ directory)
import json

# Sample data (10 entries)
tourism_data = [
    {"name": "Lalibela", "description": "Famous rock-hewn churches", "cost": 50, "interests": ["history", "culture"], "season": "Oct-Feb", "location": "Amhara"},
    {"name": "Simien Mountains", "description": "Hiking and wildlife", "cost": 80, "interests": ["nature", "adventure"], "season": "Oct-Feb", "location": "Amhara"},
    {"name": "Axum", "description": "Ancient stelae and ruins", "cost": 40, "interests": ["history", "culture"], "season": "Oct-Feb", "location": "Tigray"},
    {"name": "Gondar", "description": "Royal castles and history", "cost": 45, "interests": ["history", "culture"], "season": "Oct-Feb", "location": "Amhara"},
    {"name": "Lake Tana", "description": "Monasteries and calm waters", "cost": 30, "interests": ["nature", "culture"], "season": "Year-round", "location": "Amhara"},
    {"name": "Harar", "description": "Walled city and hyena feeding", "cost": 35, "interests": ["culture", "adventure"], "season": "Oct-Feb", "location": "Harari"},
    {"name": "Omo Valley", "description": "Tribal cultures", "cost": 100, "interests": ["culture", "adventure"], "season": "Oct-Feb", "location": "SNNPR"},
    {"name": "Bale Mountains", "description": "Rare wildlife and trekking", "cost": 70, "interests": ["nature", "adventure"], "season": "Oct-Feb", "location": "Oromia"},
    {"name": "Danakil Depression", "description": "Volcanic landscapes", "cost": 150, "interests": ["adventure", "nature"], "season": "Nov-Jan", "location": "Afar"},
    {"name": "Coffee Tour", "description": "Visit coffee farms", "cost": 25, "interests": ["culture", "food"], "season": "Nov-Jan", "location": "Oromia"},
]

# Save to JSON file
with open("tourism_data.json", "w") as f:
    json.dump(tourism_data, f, indent=4)

print("Data saved to tourism_data.json")