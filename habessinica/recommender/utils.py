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

def collaborative_filtering(user_interests, k=3, top_n=5):
    if not user_interests:
        return []

    # Generate simulated user data
    user_data, dest_names = generate_user_data()
    matrix = np.array(user_data["matrix"])  # Shape: (10 users, 10 destinations)

    # Create new_user_vector for input interests
    destinations = Destination.objects.all()
    new_user_vector = []
    for dest in destinations:
        if any(interest in dest.interests for interest in user_interests):
            new_user_vector.append(1)
        else:
            new_user_vector.append(0)
    new_user_vector = np.array([new_user_vector])  # Shape: (1, 10)

    # If no matches (all 0s), return no recommendations
    if not np.any(new_user_vector):
        return ["No recommendations found"]

    # Fit KNN model
    knn = NearestNeighbors(n_neighbors=min(k, len(matrix)), metric='cosine', algorithm='brute')
    knn.fit(matrix)

    # Find k nearest users
    distances, indices = knn.kneighbors(new_user_vector)
    similar_users = indices[0]  # e.g., [4, 1, 7]

    # Score destinations by how many similar users liked them
    dest_scores = {}
    for user_idx in similar_users:
        user_ratings = matrix[user_idx]
        for idx, rating in enumerate(user_ratings):
            if rating == 1:
                dest_scores[dest_names[idx]] = dest_scores.get(dest_names[idx], 0) + 1

    # Sort by score and limit to top_n
    sorted_recs = sorted(dest_scores.items(), key=lambda x: x[1], reverse=True)
    recommendations = [rec[0] for rec in sorted_recs[:top_n]]
    return recommendations if recommendations else ["No recommendations found"]


if __name__ == "__main__":
    user_data, dest_names = generate_user_data()
    print("Users:", user_data["users"])
    print("Matrix:", user_data["matrix"])
    print("Destinations:", dest_names)

    test_interests = ["history", "culture"]
    recs = collaborative_filtering(test_interests)
    print(f"Recommendations for {test_interests}: {recs}")