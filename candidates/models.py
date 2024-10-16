from django.db import models
from django.core.validators import RegexValidator


class Candidate(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    name = models.CharField(max_length=255, blank=False, null=False)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    country_code = models.CharField(
        max_length=5,
        default="+91",
        validators=[RegexValidator(
            regex=r'^\+\d{1,4}$',
            message="Enter a valid country code starting with + followed by 1 to 4 digits."
        )]
    )
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^\d{10,15}$',
            message="Phone number must contain 10 to 15 digits."
        )]
    )

    def __str__(self):
        return self.name