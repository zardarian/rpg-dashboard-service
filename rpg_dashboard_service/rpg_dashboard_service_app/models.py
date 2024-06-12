from django.db import models

# Create your models here.
class RpgDashboard(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    hotel_id = models.BigIntegerField(blank=True, null=True)
    period = models.DateField(blank=True, null=True)
    number_of_bookings = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rpg_dashboard'