from django.urls import path
from . import views
#git test
urlpatterns = [
    path('', views.index, name='main'),
    path('excel/', views.upload_excel_to_db, name='excel'),
    path('fault_condition/',views.fault_con, name='condition'),
    path('initial_input/',views.initial, name='initial'),
    path('flow/',views.flow, name='flow'),
    path('slider/',views.slider, name='slider'),
    path('transformer/',views.transformer, name='transformer'),
    path('ybus/',views.show_ybus, name='ybus'),
    path('zbus/',views.show_zbus, name='zbus'),
    path('sequence/', views.sequence,name='sequence'),
    path('phase/',views.phase,name='phase'),
    path('result/', views.result,name='result'),
    path('manual/', views.manual, name='manual'),
    path('manual/fileform/', views.fileform, name='fileform'),
]
