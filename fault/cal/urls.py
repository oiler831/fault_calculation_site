from django.urls import path
from . import views
#git test
urlpatterns = [
    path('', views.index, name='main'),
    path('test/',views.fault_con, name='test'),
]
