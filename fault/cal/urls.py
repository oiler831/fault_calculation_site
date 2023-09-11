from django.urls import path
from . import views
#git test
urlpatterns = [
    path('', views.upload_excel_to_db, name='main'),
    path('fault_condition/',views.fault_con, name='condition'),
    path('result/', views.result,name='result'),
    path('manual/', views.result, name='manual'),
]
