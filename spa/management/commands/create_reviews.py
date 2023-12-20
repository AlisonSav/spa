from datetime import datetime
from random import randint

from django.core.management.base import BaseCommand

from faker import Faker

from spa.models import Review


class Command(BaseCommand):
    """This custom command creates reviews"""

    def add_arguments(self, parser):
        parser.add_argument(
            "count",
            type=int,
            help="Indicates the number of Reviews to be created",
        )

    def handle(self, *args, **options):
        fake = Faker("en_US")
        Review.objects.bulk_create(
            Review(
                author_id=randint(1, 10),
                text=fake.sentence(),
                created_on=datetime.utcnow(),
            )
            for _ in range(options.get("count"))
        )
        self.stdout.write(self.style.SUCCESS(f"Added {options.get('count')} new Reviews"))
