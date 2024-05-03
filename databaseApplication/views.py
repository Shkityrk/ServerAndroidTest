import json
from operator import itemgetter

from django.apps import apps
from django.core.serializers import serialize
from django.db.models import Max
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.encoding import force_str

from .forms import StationForm, StationIdForm
from .models import StationModel


def add_data(request):
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            form.save()
            print(form.fields)
            return redirect('add_data')  # замените 'success_url_name' на имя вашего URL для перенаправления после успешного сохранения
    else:
        form = StationForm()
    return render(request, 'add.html', {'form': form})

def show_stations(request):
    stations = StationModel.objects.all()
    return render(request, 'show.html', {'stations': stations})

def edit_station(request, pk):
    station = StationModel.objects.get(pk=pk)
    if request.method == 'POST':
        form = StationForm(request.POST, instance=station)
        if form.is_valid():
            form.save()
            return redirect('show_stations')
    else:
        form = StationForm(instance=station)
    return render(request, 'edit.html', {'form': form})


def upload_json(request):
    if request.method == 'POST' and request.FILES['json_file']:
        json_file = request.FILES['json_file']
        json_data = json.load(json_file)

        for data in json_data:
            station_id = data.get('id_station')
            name = data.get('name')
            line = data.get('line')
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            width_neighbour1 = data.get('width_neighbour1')
            longitude_neighbour1 = data.get('longitude_neighbour1')
            width_neighbour2 = data.get('width_neighbour2')
            longitude_neighbour2 = data.get('longitude_neighbour2')
            is_favourite = True if data.get('is_favourite', '').lower() == 'true' else False
            alarm = True if data.get('alarm', '').lower() == 'true' else False

            StationModel.objects.create(
                station_id=station_id,
                name=name,
                line=line,
                latitude=latitude,
                longitude=longitude,
                width_neighbour1=width_neighbour1,
                longitude_neighbour1=longitude_neighbour1,
                width_neighbour2=width_neighbour2,
                longitude_neighbour2=longitude_neighbour2,
                is_favourite=is_favourite,
                alarm=alarm
            )
        subquery = StationModel.objects.values('station_id').annotate(max_id=Max('id')).values('max_id')

        # Удаляем все станции, кроме тех, у которых id равен максимальному id для их station_id
        StationModel.objects.exclude(id__in=subquery).delete()
        print("данные обновлены, дубликаты удалены")
        return render(request, 'upload_success.html')

    return render(request, 'upload.html')

def delete_station(request):
    if request.method == 'POST':
        station_id = request.POST.get('station_id')
        try:
            # Пытаемся получить все станции с заданным station_id
            stations = StationModel.objects.filter(station_id=station_id)
            if stations.count() == 1:
                station = stations.first()
                station.delete()
                return redirect('success_page')  # Перенаправляем на страницу успешного удаления
            elif stations.count() > 1:
                # Если найдено более одной станции с данным station_id, отображаем пользователю список для выбора
                return render(request, 'choose_station_to_delete.html', {'stations': stations})
            else:
                return render(request, 'error_page.html', {'error_message': 'Station does not exist.'})
        except StationModel.DoesNotExist:
            return render(request, 'error_page.html', {'error_message': 'Station does not exist.'})
    return render(request, 'delete_station.html')


def success_page(request):
    return render(request, 'success_page.html')


def choose_station_to_delete(request):
    if request.method == 'POST':
        station_id = request.POST.get('station_to_delete')
        return redirect('confirm_delete_station', station_id=station_id)
    else:
        stations = StationModel.objects.all()
        return render(request, 'choose_station_to_delete.html', {'stations': stations})

def confirm_delete_station(request):
    if request.method == 'POST':
        station_id = request.POST.get('station_to_delete')
        station = StationModel.objects.get(pk=station_id)
        station.delete()
        return redirect('success_page')  # Перенаправляем на страницу успешного удаления
    else:
        return redirect('choose_station_to_delete')  # Перенаправляем на выбор станции для удаления, если запрос не POST


def get_station_data(request):
    table_name = request.GET.get('databaseApplication')
    db_name = request.GET.get('db_name')  # Получаем имя базы данных из параметров запроса

    if not table_name or not db_name:
        return HttpResponseBadRequest("Table name and database name are required.")

    try:
        # Получаем модель по имени таблицы
        model = apps.get_model(app_label='databaseApplication', model_name="stationmodel")

    except LookupError:
        return HttpResponseBadRequest("Invalid table name.")

    # Получаем данные из указанной базы данных
    stations = model.objects.using(db_name).all().order_by('station_id')
    station_data = []
    for station in stations:
        station_dict = {}
        for field in station._meta.fields:
            # Пропускаем поле 'id'
            if field.name == 'id':
                continue
            value = getattr(station, field.name)
            if isinstance(value, timezone.datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, bytes):
                value = force_str(value)
            station_dict[field.name] = value
        station_data.append(station_dict)

    # Преобразуем список в JSON и возвращаем его
    return JsonResponse(station_data, safe=False)

from django.http import HttpResponse

def delete_dup(request):


    # Получаем максимальный id для каждой станции
    subquery = StationModel.objects.values('station_id').annotate(max_id=Max('id')).values('max_id')

    # Удаляем все станции, кроме тех, у которых id равен максимальному id для их station_id
    StationModel.objects.exclude(id__in=subquery).delete()

    return HttpResponse("Дубликаты станций успешно удалены.")
