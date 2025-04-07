# recommender/utils.py
import numpy as np
from django.conf import settings
from recommender.models import Destination
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pyowm import OWM
import datetime

def generate_user_data():
    # Fetch all destinations
    destinations = Destination.objects.all()
    dest_names = [d.name for d in destinations]
    num_destinations = len(dest_names)

    # Simulate 10 users with binary preferences (1 = liked, 0 = not liked)
    user_data = {
        "users": [],
        "matrix": []
    }
    for i in range(10):
        user_interests = np.random.choice(["history", "nature", "adventure", "culture", "food"], size=2, replace=False).tolist()
        user_vector = []
        for dest in destinations:
            if any(interest in dest.interests for interest in user_interests):
                user_vector.append(1)
            else:
                user_vector.append(0)
        user_data["users"].append({"id": f"user_{i}", "interests": user_interests})
        user_data["matrix"].append(user_vector)

    return user_data, dest_names

def collaborative_filtering(user_interests, travel_date=None, k=3, top_n=5):
    if not user_interests:
        return []

    user_data, dest_names = generate_user_data()
    matrix = np.array(user_data["matrix"])

    destinations = Destination.objects.all()
    new_user_vector = []
    for dest in destinations:
        if any(interest in dest.interests for interest in user_interests):
            new_user_vector.append(1)
        else:
            new_user_vector.append(0)
    new_user_vector = np.array([new_user_vector])

    if not np.any(new_user_vector):
        return ["No recommendations found"]

    knn = NearestNeighbors(n_neighbors=min(k, len(matrix)), metric='cosine', algorithm='brute')
    knn.fit(matrix)

    distances, indices = knn.kneighbors(new_user_vector)
    similar_users = indices[0]

    dest_scores = {}
    for user_idx in similar_users:
        user_ratings = matrix[user_idx]
        for idx, rating in enumerate(user_ratings):
            if rating == 1:
                dest = destinations[idx]
                # Apply seasonal filter if travel_date provided
                if travel_date and not is_season_match(dest.season, travel_date):
                    continue
                # Check weather (uncomment when API key is ready)
                # if not get_weather(dest.location, settings.OPENWEATHER_API_KEY):
                #     continue
                dest_scores[dest_names[idx]] = dest_scores.get(dest_names[idx], 0) + 1

    sorted_recs = sorted(dest_scores.items(), key=lambda x: x[1], reverse=True)
    recommendations = [rec[0] for rec in sorted_recs[:top_n]]
    return recommendations if recommendations else ["No recommendations found"]

def get_destination_texts():
    destinations = Destination.objects.all()
    texts = []
    dest_names = []
    for dest in destinations:
        # Combine description and interests into one string
        text = f"{dest.description} {' '.join(dest.interests)}"
        texts.append(text)
        dest_names.append(dest.name)
    return texts, dest_names

def content_based_filtering(user_interests, travel_date=None, top_n=5):
    if not user_interests:
        return []

    texts, dest_names = get_destination_texts()
    destinations = Destination.objects.all()

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    user_vector = vectorizer.transform([" ".join(user_interests)])

    similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()
    top_indices = similarities.argsort()[::-1]
    
    recommendations = []
    for idx in top_indices:
        if similarities[idx] > 0:
            dest = destinations[idx]
            # Apply seasonal filter if travel_date provided
            if travel_date and not is_season_match(dest.season, travel_date):
                continue
            # Check weather (uncomment when API key is ready)
            if not get_weather(dest.location, settings.OPENWEATHER_API_KEY):
                continue
            recommendations.append(dest_names[idx])
            if len(recommendations) >= top_n:
                break

    return recommendations if recommendations else ["No recommendations found"]

def is_season_match(dest_season, travel_date=None):
    # Map season strings to months
    season_months = {
        "Oct-Feb": range(10, 13),  # Oct-Dec (wraps to next year)
        "Nov-Jan": range(11, 13),  # Nov-Dec (wraps to next year)
        "Year-round": range(1, 13),
    }
    # Handle year-wrap for Oct-Feb and Nov-Jan
    if travel_date is None:
        return True  # No date provided, assume match
    if dest_season == "Oct-Feb":
        return travel_date.month in [10, 11, 12] or travel_date.month in [1, 2]
    elif dest_season == "Nov-Jan":
        return travel_date.month in [11, 12] or travel_date.month == 1
    elif dest_season == "Year-round":
        return True
    return False

def get_weather(location, api_key):
    owm = OWM(api_key)
    mgr = owm.weather_manager()
    try:
        observation = mgr.weather_at_place(location + ",ET")  # ET = Ethiopia
        weather = observation.weather
        temp = weather.temperature('celsius')['temp']
        status = weather.status.lower()  # e.g., "clear", "rain"
        return temp > 15 and "rain" not in status  # Simple "good weather" check
    except Exception:
        return True  # Fallback to True if API fails

if __name__ == "__main__":
    user_data, dest_names = generate_user_data()
    print("Users:", user_data["users"])
    print("Matrix:", user_data["matrix"])
    print("Destinations:", dest_names)

    test_interests = ["history", "culture"]
    recs = collaborative_filtering(test_interests)
    print(f"Recommendations for {test_interests}: {recs}")