from django.shortcuts import render, redirect
from .models import FaultCondition

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
        impedence_R = request.POST['impedence_R']
        impedence_X = request.POST['impedence_X']
        if is_bus_fault:
            fault_bus = request.POST['fault_bus']
            fault_line_1 = 0
            fault_line_2 = 0
            line_percentage = 0
        else:
            fault_bus = 0
            fault_line_1 = request.POST['fault_line_1']
            fault_line_2 = request.POST['fault_line_2']
            line_percentage = request.POST['line_percentage']
        if len(request.POST.getlist('is_shunt')):
            is_shunt = True
        else:
            is_shunt = False
        if len(request.POST.getlist('is_load_effect')):
            is_load_effect = True
        else:
            is_load_effect = False
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