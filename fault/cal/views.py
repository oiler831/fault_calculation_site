from django.shortcuts import render, redirect
from .models import FaultCondition

# Create your views here.
def index(request):
    return render(request,'cal/main.html')

def manual(request):
    return render(request,'cal/main.html')

def fault_con(request):
    if request.method == 'POST':
        new_con = FaultCondition(
            basemva = request.POST['basemva'],
            is_flow = request.POST['is_flow'],
            fault_type = request.POST['fault_type'],
            is_bus_fault = request.POST['is_bus_fault'],
            fault_bus = request.POST['fault_bus'],
            fault_line_1 = request.POST['fault_line_1'],
            fault_line_2 = request.POST['fault_line_2'],
            line_percentage = request.POST['line_percentage'],
            impedence_R = request.POST['impedence_R'],
            impedence_X = request.POST['impedence_X'],
        )
        if len(request.POST.getlist('is_shunt')):
            FaultCondition.is_shunt = True
        else:
            FaultCondition.is_shunt = False
        if len(request.POST.getlist('is_load_effect')):
            FaultCondition.is_load_effect = True
        else:
            FaultCondition.is_load_effect = False    
        new_con.save()
        return redirect('main')
    return render(request, 'cal/fault_con.html')