from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^soap_service/', views.my_soap_application),
]