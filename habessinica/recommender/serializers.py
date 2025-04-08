# recommender/serializers.py
from rest_framework import serializers
from .models import Destination

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['name', 'description', 'cost', 'interests', 'season', 'location']