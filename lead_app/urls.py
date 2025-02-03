from django.urls import path
from .views import receive_wheel_lead

urlpatterns = [
    path('receive_wheel_lead/', receive_wheel_lead, name='receive_wheel_lead'),
]
