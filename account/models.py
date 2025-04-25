# models.py
from django.contrib.auth.models import User
from django.db import models
TITLE_CHOICES = [
    ('', 'Select a title'),  # Empty default option
    ('dr', 'Dr.'),
    ('mr', 'Mr.'),
    ('mrs', 'Mrs.'),
    ('ms', 'Ms.'),
    ('prof', 'Prof.'),
    ('rev', 'Rev.'),
]

DEGREE_CHOICES = [
    ('', 'Select a degree'),
    ('phd', 'PhD'),
    ('md', 'MD'),
    ('jd', 'JD'),
    ('mba', 'MBA'),
    ('ma', 'MA'),
    ('ms', 'MS'),
    ('ba', 'BA'),
    ('bs', 'BS'),
    ('other', 'Other'),
]

PHONE_TYPE_CHOICES = [
    ('mobile', 'Mobile'),
    ('home', 'Home'),
    ('work', 'Work'),
    ('assistant', 'Assistant'),
    ('other', 'Other'),
]

ADDRESS_TYPE_CHOICES = [
    ('work', 'Work'),
    ('home', 'Home'),
    ('other', 'Other'),
]


class AffiliationInfo(models.Model):
    # Institution Related Information // Affiliation
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100, blank=True, null=True)
    institution = models.CharField(max_length=200)
    department = models.CharField(max_length=100, blank=True, null=True)
    street_address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state_province = models.CharField(max_length=100, blank=True, null=True)
    zip_postal_code = models.CharField(max_length=20, blank=True, null=True)
    country_region = models.CharField(max_length=100)
    address_is_for = models.CharField(
        max_length=20, choices=ADDRESS_TYPE_CHOICES)
    available_as_reviewer = models.BooleanField(default=False)


class PersonalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=20, choices=TITLE_CHOICES, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    degree = models.CharField(
        max_length=20, choices=DEGREE_CHOICES, blank=True, null=True)
    email = models.EmailField()
    primary_phone = models.CharField(max_length=20)
    primary_phone_type = models.CharField(
        max_length=20, choices=PHONE_TYPE_CHOICES)
    secondary_phone = models.CharField(max_length=20, blank=True, null=True)
    secondary_phone_type = models.CharField(
        max_length=20, choices=PHONE_TYPE_CHOICES, blank=True, null=True)
    

# models.py
# from django.db import models
# from django.contrib.auth.models import User



# TITLE_CHOICES = {
#     "MR": "Mr.",
#     "MRS": "Mrs.",
#     "MS": "Ms.",
# }


# class Author(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

#     name = models.CharField(max_length=100,blank=False)
#     title = models.CharField(max_length=3, choices=TITLE_CHOICES)
#     birth_date = models.DateField(blank=True, null=True)

#     def __str__(self):
#         return self.name 