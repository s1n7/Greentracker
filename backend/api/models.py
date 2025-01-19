from django.db import models


from django.contrib.auth.models import AbstractUser
from django.db import models

# User model
class User(AbstractUser):  # extension to the default User model
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    # password hashing done by default
    created_at = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Custom related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Custom related_name
        blank=True
    )


# Activity model
class Activity(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50)  # e.g. transport, energy
    co2_per_unit = models.FloatField()  # CO₂ in kg pro unit (e.g. per km, per kWh)

    def __str__(self):
        return self.name

# Entry model
class UserEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    quantity = models.FloatField()  # activity amount (e.g. km, kWh)
    date = models.DateField()
    total_co2 = models.FloatField()  # automatically calculated based on activity and quantity

    def save(self, *args, **kwargs):
        # calculate total_co2 based on activity
        self.total_co2 = self.quantity * self.activity.co2_per_unit
        super().save(*args, **kwargs)  # standard save mode

    def __str__(self):
        return f"{self.activity.name} - {self.total_co2} kg CO₂"