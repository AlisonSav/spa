from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from faker import Faker


class Command(BaseCommand):
    """This custom command creates users"""

    User = get_user_model()
    fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument(
            "count",
            type=int,
            choices=range(1, 11),
            help="Indicates the number of users to be created",
        )

    def handle(self, *args, **options):
        fake = Faker("en_US")
        User = get_user_model()
        User.objects.bulk_create(
            User(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
            for _ in range(options.get("count"))
        )
        self.stdout.write(self.style.SUCCESS(f"Added {options.get('count')} new Authors"))
