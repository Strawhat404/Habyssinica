# recommender/utils.py
import numpy as np
from recommender.models import Destination
from sklearn.neighbors import NearestNeighbors

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

def collaborative_filtering(user_interests, k=3):
    if not user_interests:
        return []  # Return empty list if no interests provided

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

    knn = NearestNeighbors(n_neighbors=min(k, len(matrix)), metric='cosine', algorithm='brute')
    knn.fit(matrix)

    distances, indices = knn.kneighbors(new_user_vector)
    similar_users = indices[0]
    recommended_indices = set()
    for user_idx in similar_users:
        user_ratings = matrix[user_idx]
        recommended_indices.update(np.where(user_ratings == 1)[0])

    recommendations = [dest_names[idx] for idx in recommended_indices]
    return recommendations if recommendations else ["No recommendations found"]

if __name__ == "__main__":
    user_data, dest_names = generate_user_data()
    print("Users:", user_data["users"])
    print("Matrix:", user_data["matrix"])
    print("Destinations:", dest_names)

    test_interests = ["history", "culture"]
    recs = collaborative_filtering(test_interests)
    print(f"Recommendations for {test_interests}: {recs}")