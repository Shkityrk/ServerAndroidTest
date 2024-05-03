from django.db import models

class StationModel(models.Model):
    station_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True)
    line = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=50, blank=True, null=True)
    width_neighbour1 = models.CharField(max_length=50, blank=True, null=True)
    longitude_neighbour1 = models.CharField(max_length=50, blank=True, null=True)
    width_neighbour2 = models.CharField(max_length=50, blank=True, null=True)
    longitude_neighbour2 = models.CharField(max_length=50, blank=True, null=True)
    is_favourite = models.BooleanField(default=False, blank=True, null=True)
    alarm = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name