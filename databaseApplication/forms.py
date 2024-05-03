from django import forms
from .models import StationModel

class StationForm(forms.ModelForm):
    class Meta:
        model = StationModel
        fields = '__all__'
        widgets = {
            'station_id': forms.NumberInput(attrs={'required': False}),
            'name': forms.TextInput(attrs={'required': False}),
            'line': forms.TextInput(attrs={'required': False}),
            'latitude': forms.TextInput(attrs={'required': False}),
            'longitude': forms.TextInput(attrs={'required': False}),
            'width_neighbour1': forms.TextInput(attrs={'required': False}),
            'longitude_neighbour1': forms.TextInput(attrs={'required': False}),
            'width_neighbour2': forms.TextInput(attrs={'required': False}),
            'longitude_neighbour2': forms.TextInput(attrs={'required': False}),
            'is_favourite': forms.CheckboxInput(attrs={'required': False}),
            'alarm': forms.TextInput(attrs={'required': False}),
        }

class StationIdForm(forms.Form):
    station_id = forms.IntegerField(label='Station ID')