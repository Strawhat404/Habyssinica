# recommender/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import collaborative_filtering, content_based_filtering
from .models import Destination
from .serializers import DestinationSerializer
from datetime import datetime

class CollaborativeRecommendView(APIView):
    def get(self, request):
        interests = request.query_params.get('interests', '').split(',')
        travel_date_str = request.query_params.get('travel_date', None)
        travel_date = datetime.strptime(travel_date_str, '%Y-%m-%d') if travel_date_str else None

        if not interests or interests == ['']:
            return Response({"recommendations": []}, status=status.HTTP_200_OK)

        rec_names = collaborative_filtering(interests, travel_date)
        if rec_names == ["No recommendations found"]:
            return Response({"recommendations": []}, status=status.HTTP_200_OK)

        destinations = Destination.objects.filter(name__in=rec_names)
        serializer = DestinationSerializer(destinations, many=True)
        return Response({"recommendations": serializer.data}, status=status.HTTP_200_OK)

class ContentRecommendView(APIView):
    def get(self, request):
        interests = request.query_params.get('interests', '').split(',')
        travel_date_str = request.query_params.get('travel_date', None)
        travel_date = datetime.strptime(travel_date_str, '%Y-%m-%d') if travel_date_str else None

        if not interests or interests == ['']:
            return Response({"recommendations": []}, status=status.HTTP_200_OK)

        rec_names = content_based_filtering(interests, travel_date)
        if rec_names == ["No recommendations found"]:
            return Response({"recommendations": []}, status=status.HTTP_200_OK)

        destinations = Destination.objects.filter(name__in=rec_names)
        serializer = DestinationSerializer(destinations, many=True)
        return Response({"recommendations": serializer.data}, status=status.HTTP_200_OK)