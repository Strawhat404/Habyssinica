# recommender/utils.py
import os
import django
import numpy as np
from sklearn.neighbors import NearestNeighbors

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habessinica.settings')
django.setup()

from recommender.models import Destination

def generate_user_data():
    # Fetch all destinations
    destinations = Destination.objects.all()
    dest_names = [d.name for d in destinations]
    num_destinations = len(dest_names)

    # Simulate 10 users with binary preferences (1 = liked, 0 = not liked)
    # Based on interests matching
    user_data = {
        "users": [],
        "matrix": []
    }
    for i in range(10):
        user_interests = np.random.choice(["history", "nature", "adventure", "culture", "food"], size=2, replace=False).tolist()
        user_vector = []
        for dest in destinations:
            # 1 if any user interest matches destination interest, else 0
            if any(interest in dest.interests for interest in user_interests):
                user_vector.append(1)
            else:
                user_vector.append(0)
        user_data["users"].append({"id": f"user_{i}", "interests": user_interests})
        user_data["matrix"].append(user_vector)

    return user_data, dest_names

if __name__ == "__main__":
    user_data, dest_names = generate_user_data()
    print("Users:", user_data["users"])
    print("Matrix:", user_data["matrix"])
    print("Destinations:", dest_names)
    
from sklearn.neighbors import NearestNeighbors

def collaborative_filtering(user_interests, k=3):
    # Generate user data
    user_data, dest_names = generate_user_data()
    matrix = np.array(user_data["matrix"])

    # Simulate new user's preference vector based on interests
    destinations = Destination.objects.all()
    new_user_vector = []
    for dest in destinations:
        if any(interest in dest.interests for interest in user_interests):
            new_user_vector.append(1)
        else:
            new_user_vector.append(0)
    new_user_vector = np.array([new_user_vector])

    # Fit KNN model
    knn = NearestNeighbors(n_neighbors=k, metric='cosine', algorithm='brute')
    knn.fit(matrix)

    # Find k nearest users
    distances, indices = knn.kneighbors(new_user_vector)

    # Get recommendations from similar users
    similar_users = indices[0]
    recommended_indices = set()
    for user_idx in similar_users:
        user_ratings = matrix[user_idx]
        # Add destinations liked by similar users (1s)
        recommended_indices.update(np.where(user_ratings == 1)[0])

    # Convert indices to destination names
    recommendations = [dest_names[idx] for idx in recommended_indices]
    return recommendations

if __name__ == "__main__":
    # Test the function
    test_interests = ["history", "culture"]
    recs = collaborative_filtering(test_interests)
    print(f"Recommendations for {test_interests}: {recs}")