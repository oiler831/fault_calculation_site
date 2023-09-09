from django.urls import path
from . import views
#git test
urlpatterns = [
    path('', views.index),
]
