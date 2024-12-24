from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.


class Feedback(models.Model):
    deity_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    tilak_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    leela_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    samatha_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    deposit_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    water_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    wash_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    accessibility_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    parking_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    food_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    shopping_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    kids_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    entry_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    directions_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    overall_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    feedback = models.TextField(blank=True, null=True)
    contact = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Feedback #{self.id} - {self.created_at.astimezone(timezone.get_current_timezone()).strftime('%Y-%m-%d %H:%M:%S %Z')}"