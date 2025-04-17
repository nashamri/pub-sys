from django.db import models

# Create your models here.

class Affiliation(models.Model):
    name = models.CharField(max_length=255, help_text="Name of the affiliation")
    address = models.TextField(help_text="Full address of the affiliation")
    country = models.CharField(max_length=100, help_text="Country where the affiliation is located")
    phone = models.CharField(max_length=50, help_text="Contact phone number")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Affiliation"
        verbose_name_plural = "Affiliations"
