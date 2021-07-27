from django import forms
import django_filters

from .models import Attendence

class AttendenceFilter(django_filters.FilterSet):
    Student_ID = django_filters.CharFilter(widget = forms.TextInput(attrs={"class": "form-control"}))
    date = django_filters.CharFilter(widget = forms.TextInput(attrs={"class": "form-control"}))
    year = django_filters.CharFilter(widget = forms.TextInput(attrs={"class": "form-control"}))
    period = django_filters.CharFilter(widget = forms.TextInput(attrs={"class": "form-control"}))
    class Meta:
        model = Attendence
        fields = ['Student_ID', 'date', 'year', 'period']
    