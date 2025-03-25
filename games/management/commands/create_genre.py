from django.core.management import BaseCommand

from games.models import Genre


genres = [
    "RPG", "Action", "Horror", "Detective", "Races", "Quests", "Metroidvane", "Shooters", "Online"
]

class Command(BaseCommand):
    def handle(self, *args, **options):
        for genre in genres:
            Genre.objects.create(name=f"{genre}")

        self.stdout.write(self.style.SUCCESS(f"Добавлено {len(genre)} жанров в базу данных!"))

