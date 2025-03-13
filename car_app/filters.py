from django_filters import FilterSet
from .models import Car

class CarFilter(FilterSet):
    class Meta:
        model = Car
        fields = {
            'car_name': ['exact'],
            'price': ['gt', 'lt']
        }