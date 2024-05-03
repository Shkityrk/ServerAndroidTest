from django.urls import path
from .views import *

urlpatterns = [
    path('add/', add_data, name='add_data'),

    path('show/', show_stations, name="show"),

    path('stations/', show_stations, name='show_stations'),
    path('stations/<int:pk>/edit/', edit_station, name='edit_station'),
    path('upload/', upload_json, name='upload_json'),
    path('delete-station/', delete_station, name='delete_station'),
    path('choose-station-to-delete/', choose_station_to_delete, name='choose_station_to_delete'),
    path('confirm-delete-station/', confirm_delete_station, name='confirm_delete_station'),
    # URL для подтверждения удаления станции
    path('success/', success_page, name='success_page'),  # URL для страницы успешного удаления
    path('get-stations/', get_station_data, name='get_station_data'),

    path('del-dup/', delete_dup, name="deleteDup"),
    path('get_station_data/', get_station_data, name='get_station_data'),


]
