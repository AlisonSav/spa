from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):  # noqa DJ10, DJ11
    email = models.EmailField(unique=True)
    avatar = models.ImageField(
        "avatar",
        upload_to="images",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "gif", "png"])],
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.username}, {self.email}"

    def get_absolute_url(self):
        return reverse("spa:author_detail", kwargs={"pk": self.pk})


class Review(models.Model):  # noqa DJ10, DJ11
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)
    file = models.ImageField(
        "file",
        upload_to="images",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "gif", "png"])],
    )

    def __str__(self):
        return f"{self.author} - {self.text[:30]}... Created on: {self.created_on:'%d.%m.%Y, %H:%m'}. "

    def get_absolute_url(self):
        return reverse("spa:review_detail", kwargs={"pk": self.pk})


class Comment(models.Model):  # noqa DJ10, DJ11
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, blank=True)
    author = models.CharField(max_length=50)
    comment_text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"{self.comment_text}. Author: {self.author}. {self.created_on:'%d.%m.%Y, %H:%m'}, {self.review}, "
            f"{self.parent_comment}"
        )
