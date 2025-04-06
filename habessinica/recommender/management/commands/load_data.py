# recommender/management/commands/load_data.py
from django.core.management.base import BaseCommand
import json
from recommender.models import Destination

class Command(BaseCommand):
    help = 'Loads tourism data from JSON file into the database'

    def handle(self, *args, **kwargs):
        with open('tourism_data_cleaned.json', 'r') as f:
            data = json.load(f)

        for entry in data:
            # Check if destination already exists to avoid duplicates
            if not Destination.objects.filter(name=entry['name']).exists():
                Destination.objects.create(
                    name=entry['name'],
                    description=entry['description'],
                    cost=entry['cost'],
                    interests=entry['interests'],
                    season=entry['season'],
                    location=entry['location']
                )
                self.stdout.write(self.style.SUCCESS(f"Added {entry['name']}"))
            else:
                self.stdout.write(f"Skipped {entry['name']} - already exists")