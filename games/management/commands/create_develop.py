from django.core.management import BaseCommand

from games.models import Developer


developer = [
    "Sony", "CDproject", "Cherry", "EA", "Ubisoft", "Bethesda", "VAlve", "Konamy", "Capcom"
]

class Command(BaseCommand):
    def handle(self, *args, **options):
        for develop in developer:
            Developer.objects.create(name=f"{develop}")

        self.stdout.write(self.style.SUCCESS(f"Добавлено {len(develop)} разработчиков в базу данных!"))

