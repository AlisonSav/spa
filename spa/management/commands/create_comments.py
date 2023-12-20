import random
from datetime import datetime
from random import randint

from django.core.management.base import BaseCommand

from faker import Faker

from spa.models import Review, Comment, CustomUser


class Command(BaseCommand):
    """This custom command creates comments as comment_parent and after creates nested comments"""

    def add_arguments(self, parser):
        parser.add_argument(
            "count",
            type=int,
            help="Indicates the number of Reviews to be created",
        )

    def handle(self, *args, **options):
        fake = Faker("en_US")
        Comment.objects.bulk_create(
            Comment(
                review=Review.objects.get(id=randint(1, 10)),
                author=CustomUser.objects.get(id=randint(1, 10)),
                comment_text=fake.sentence(),
                created_on=datetime.utcnow(),
            )
            for _ in range(options.get("count"))
        )
        reviews = Review.objects.get(id=randint(1, 10))
        parent_comments = Comment.objects.filter(review=reviews)
        comment = random.choice(parent_comments)
        Comment.objects.bulk_create(
            Comment(
                author=CustomUser.objects.get(id=randint(1, 10)),
                comment_text=fake.sentence(),
                created_on=datetime.utcnow(),
                parent_comment=comment,
            )
            for _ in range(options.get("count"))
        )
        self.stdout.write(self.style.SUCCESS(f"Added {options.get('count')} new Comments"))
