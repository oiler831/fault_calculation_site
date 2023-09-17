from django.urls import path
from . import views
#git test
urlpatterns = [
    path('', views.index, name='main'),
    path('excel/', views.upload_excel_to_db, name='excel'),
    path('fault_condition/',views.fault_con, name='condition'),
    path('result/', views.result,name='result'),
    path('manual/', views.manual, name='manual'),
]
