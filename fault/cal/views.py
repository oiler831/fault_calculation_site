from django.shortcuts import render, redirect
from .models import FaultCondition, BusData, LineData, ExcelFile
import pandas as pd
import os

# Create your views here.
def index(request):
    return render(request,'cal/main.html')

def manual(request):
    return render(request,'cal/main.html')

def fault_con(request):
    if request.method == 'POST':
        basemva = request.POST['basemva']
        is_flow = request.POST['is_flow']
        fault_type = request.POST['fault_type']
        is_bus_fault = request.POST['is_bus_fault']
        fault_bus = request.POST.get('fault_bus',0)
        fault_line_1 = request.POST.get('fault_line_1',0)
        fault_line_2 = request.POST.get('fault_line_2',0)
        line_percentage = request.POST.get('line_percentage',0)
        impedence_R = request.POST['impedence_R']
        impedence_X = request.POST['impedence_X']
        is_shunt = request.POST.get('is_shunt', False)
        is_load_effect = request.POST.get('is_load_effect', False)
        new_con = FaultCondition(
            basemva = basemva,
            is_flow = is_flow,
            fault_type = fault_type,
            is_bus_fault = is_bus_fault,
            fault_bus = fault_bus,
            fault_line_1 = fault_line_1,
            fault_line_2 = fault_line_2,
            line_percentage = line_percentage,
            impedence_R = impedence_R,
            impedence_X = impedence_X,
            is_shunt =is_shunt,
            is_load_effect = is_load_effect
        )
        new_con.save()
        return redirect('main')
    return render(request, 'cal/fault_con.html')


def upload_excel_to_db(request):
    if request.method == 'POST':
        excel_file = request.FILES['excelFile']
        new_file = ExcelFile(file = excel_file)
        new_file.save()
        bus_df = pd.read_excel(excel_file,header=None,sheet_name=0)
        line_df = pd.read_excel(excel_file,header=None,sheet_name=1)
        for i in range(len(bus_df)):
            BusData.objects.create(bus_num = bus_df[0][i])
        for i in range(len(line_df)):
            LineData.objects.create(to_bus = line_df[0][i],from_bus = line_df[1][i])
        return redirect('condition')
    return render(request,'cal/main.html')
