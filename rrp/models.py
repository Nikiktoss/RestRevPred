from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


def user_directory_path_pdf(instance, filename):
    return 'pdf_files/user_{0}/{1}'.format(instance.user.id, filename)


def user_directory_path_json(instance, filename):
    return 'json_files/user_{0}/{1}'.format(instance.user.id, filename)


class User(AbstractUser):
    photo = models.ImageField(upload_to="media/user_pictures/%Y-%m-%d/", verbose_name="Account photo", blank=True)
    creation_date = models.DateField(auto_now_add=True, verbose_name="Date of creation", blank=True)
    slug = models.SlugField(max_length=75, unique=True, blank=True, verbose_name="URL")
    birth_date = models.DateField(verbose_name="Date of birth", blank=True, null=True)
    additional_data = models.TextField(blank=True, verbose_name="About you")
    company = models.CharField(max_length=75, blank=True, verbose_name="Company")
    number_of_predictions = models.IntegerField(verbose_name="Number of calculations", default=0)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.username, self.email)
        super(User, self).save(*args, **kwargs)


class PredictionResult(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    revenue = models.DecimalField(verbose_name="Predict revenue",  max_digits=20, decimal_places=9)
    date_of_calculations = models.DateField(verbose_name="Date of calculations", auto_now_add=True)
    pdf_file = models.FileField(verbose_name="PDF File", upload_to=user_directory_path_pdf, blank=True, null=True)
    json_file = models.FileField(verbose_name="JSON File", upload_to=user_directory_path_json, blank=True, null=True)
