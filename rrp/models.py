from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class User(AbstractUser):
    photo = models.ImageField(upload_to="media/user_pictures/%Y-%m-%d/", verbose_name="Account photo", blank=True)
    creation_date = models.DateField(auto_now_add=True, verbose_name="Date of creation", blank=True)
    slug = models.SlugField(max_length=75, unique=True, blank=True, verbose_name="URL")
    birth_date = models.DateField(verbose_name="Date of birth", blank=True)
    additional_data = models.TextField(blank=True, verbose_name="About you")
    company = models.CharField(max_length=75, blank=True, verbose_name="Company")

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.username, self.email)
        super(User, self).save(*args, **kwargs)
