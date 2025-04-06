import json

with open("tourism_data.json", "r") as f:
    data = json.load(f)

def preprocess_entry(entry):
    # Ensure all fields exist, set defaults if missing
    entry.setdefault("name", "Unknown")
    entry.setdefault("description", "")
    entry.setdefault("cost", 0)
    entry.setdefault("interests", [])
    entry.setdefault("season", "Year-round")
    entry.setdefault("location", "Ethiopia")

    # Normalize text
    entry["description"] = entry["description"].lower().strip()
    entry["name"] = entry["name"].strip()

    # Validate cost
    if not isinstance(entry["cost"], (int, float)) or entry["cost"] < 0:
        entry["cost"] = 0

    return entry

# Apply preprocessing
cleaned_data = [preprocess_entry(entry) for entry in data]

# Save cleaned data
with open("tourism_data_cleaned.json", "w") as f:
    json.dump(cleaned_data, f, indent=4)

print("Cleaned data saved to tourism_data_cleaned.json")