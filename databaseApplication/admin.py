from django.contrib import admin

from .models import *
# Register your models here.

@admin.register(StationModel)
class StationsAdmin(admin.ModelAdmin):
    list_display = (
        "station_id",
        "name",
        "line",
        "latitude",
        "longitude",
        "width_neighbour1",
        "longitude_neighbour1",
        "width_neighbour2",
        "longitude_neighbour2",
        "is_favourite",
        "alarm")
    list_display_links = (
        "station_id",
        "name",
        "line",)

    ordering = ['station_id']


# admin.site.register(StationModel, StationsAdmin)