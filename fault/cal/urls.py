from django.urls import path
from . import views
#git test
urlpatterns = [
    path('', views.index, name='main'),
    path('excel/', views.upload_excel_to_db, name='excel'),
    path('fault_condition/',views.fault_con, name='condition'),
    #path('circuit_data/', views.circuit, name='circuit'),
    path('ybus/',views.show_ybus, name='ybus'),
    path('zbus/',views.show_zbus, name='zbus'),
    path('sequence/', views.sequence,name='sequence'),
    path('phase/',views.phase,name='phase'),
    path('result/', views.result,name='result'),
    path('manual/', views.manual, name='manual'),
]
