# Generated by Django 5.0 on 2023-12-20 13:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("spa", "0002_review_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="avatar",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="images",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["jpg", "jpeg", "gif", "png"]
                    )
                ],
                verbose_name="avatar",
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="file",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="images",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["jpg", "jpeg", "gif", "png"]
                    )
                ],
                verbose_name="file",
            ),
        ),
    ]
