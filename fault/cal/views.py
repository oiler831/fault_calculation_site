from django.shortcuts import render, redirect
from .models import (FaultCondition, BusData, LineData, ExcelFile,FaultLineData,FaultBusData,
                    ThreeFaultI,ThreeFaultV,OtherFaultI,OtherFaultV,conditionCheck,ThreeZbus,ThreeZbusSource,
                    OtherZbusSource,OtherZbus,negativeZbusSource,zeroZbusSource,isExample,OthersequenceI,OthersequenceV,
                    Afterflow,SliderLine,Sliderbus,resultfile, errorcheck)
import pandas as pd
import numpy as np
import math
from pathlib import Path
from django.core.files import File
import os

# Create your views here.
def index(request):
    clear = errorcheck.objects.all()
    clear.delete()
    errorcheck.objects.create(errornum=0,find_check=True)
    return render(request,'cal/main.html')

def manual(request):
    return render(request,'cal/manual.html')

def fileform(request):
    return render(request,'cal/input_data.html')


def upload_excel_to_db(request):
    clear = BusData.objects.all()
    clear.delete()
    clear = LineData.objects.all()
    clear.delete()
    clear = conditionCheck.objects.all()
    clear.delete()
    clear = ExcelFile.objects.all()
    clear.delete()
    clear = isExample.objects.all()
    clear.delete()
    if request.method == 'POST':
        if request.POST['isexample'] == "True":
            check = request.POST.get('exampleselect',False)
            if check == False:
                e_num = errorcheck.objects.get(find_check=True)
                return render(request,'cal/file.html',context={'errornum':e_num})
            else:
                if request.POST['exampleselect']=='1':
                    excel_file="/home/jin/fault_calculation_site/fault/media/example/Glover_9.8.xlsx"
                elif request.POST['exampleselect']=='2':
                    excel_file="/home/jin/fault_calculation_site/fault/media/example/Saadat9.8.xlsx"
                elif request.POST['exampleselect']=='3':
                    excel_file="/home/jin/fault_calculation_site/fault/media/example/Saadat10.7.xlsx"
                elif request.POST['exampleselect']=='4':
                    excel_file = "/home/jin/fault_calculation_site/fault/media/example/Saadat9.9-1.xlsx"
                elif request.POST['exampleselect']=='5':
                    excel_file = "/home/jin/fault_calculation_site/fault/media/example/Saadat9.9-2.xlsx"
                elif request.POST['exampleselect']=='6':
                    excel_file = "/home/jin/fault_calculation_site/fault/media/example/Saadat10.8.xlsx"
                elif request.POST['exampleselect']=='7':
                    excel_file = "/home/jin/fault_calculation_site/fault/media/example/contest.xlsx"
        else:
            excel_file = request.FILES.get('excelFile',False)
            if excel_file == False:
                e_num = errorcheck.objects.get(find_check=True)
                e_num.errornum = 1
                e_num.save()
                return render(request,'cal/file.html',context={'errornum':e_num})
            else:
                filename, fileExtension = os.path.splitext(str(excel_file))
                if fileExtension != ".xlsx":
                    e_num = errorcheck.objects.get(find_check=True)
                    e_num.errornum = 2
                    e_num.save()
                    return render(request,'cal/file.html',context={'errornum':e_num})
                find_file = True
                new_file = ExcelFile(file = excel_file, find_file = find_file)
                new_file.save()
        isExample.objects.create(isex=request.POST['isexample'],exampleNumber=request.POST.get('exampleselect'),find_ex=True)
        bus_df = pd.read_excel(excel_file,header=None,sheet_name=0)
        line_df = pd.read_excel(excel_file,header=None,sheet_name=1)
        if len(bus_df.columns) != 10 and len(bus_df.columns) !=3:
            e_num = errorcheck.objects.get(find_check=True)
            e_num.errornum = 3
            e_num.save()
            return render(request,'cal/file.html',context={'errornum':e_num})
        if len(line_df.columns) != 12 and len(line_df.columns) !=6:
            e_num = errorcheck.objects.get(find_check=True)
            e_num.errornum = 4
            e_num.save()
            return render(request,'cal/file.html',context={'errornum':e_num})
        if len(bus_df.columns) != 10  :
            is_flow = False
        else:
            is_flow = True
        if len(line_df.columns) != 12:
            is_not_symmetry = False
        else:
            is_not_symmetry = True
        try:
            if is_flow:
                for i in range(len(bus_df)):
                    BusData.objects.create(bus_num = bus_df[0][i],Voltage_Mag=bus_df[1][i],Voltage_Deg=bus_df[2][i],Generator_MW=bus_df[3][i],
                                        Generator_Mvar = bus_df[4][i],Load_MW=bus_df[5][i],Load_Mvar=bus_df[6][i],Qmax=bus_df[7][i],
                                        Qmin=bus_df[8][i], Bus_Code=bus_df[9][i])
            else:
                for i in range(len(bus_df)):
                    BusData.objects.create(bus_num = bus_df[0][i],Voltage_Mag=bus_df[1][i],Voltage_Deg=bus_df[2][i])
            if is_not_symmetry:
                for i in range(len(line_df)):
                    if line_df[0][i] == 0:
                        if line_df[11][i] == 4:
                            LineData.objects.create(from_bus = line_df[1][i],to_bus = line_df[0][i],R = line_df[2][i],X = line_df[3][i],
                                            B = line_df[4][i],negative_R = line_df[5][i],negative_X = line_df[6][i],zero_R = line_df[7][i],
                                            zero_X = line_df[8][i],Xn = line_df[9][i],zero_B = line_df[10][i],line_type = 3)
                        else:
                            LineData.objects.create(from_bus = line_df[1][i],to_bus = line_df[0][i],R = line_df[2][i],X = line_df[3][i],
                                            B = line_df[4][i],negative_R = line_df[5][i],negative_X = line_df[6][i],zero_R = line_df[7][i],
                                            zero_X = line_df[8][i],Xn = line_df[9][i],zero_B = line_df[10][i],line_type = line_df[11][i])
                    else:
                        LineData.objects.create(from_bus = line_df[0][i],to_bus = line_df[1][i],R = line_df[2][i],X = line_df[3][i],
                                            B = line_df[4][i],negative_R = line_df[5][i],negative_X = line_df[6][i],zero_R = line_df[7][i],
                                            zero_X = line_df[8][i],Xn = line_df[9][i],zero_B = line_df[10][i],line_type = line_df[11][i])
            else:
                for i in range(len(line_df)):
                    if line_df[0][i] == 0:
                        if line_df[5][i] == 4:
                            LineData.objects.create(from_bus = line_df[1][i],to_bus = line_df[0][i],R = line_df[2][i],X = line_df[3][i],B = line_df[4][i],line_type=3)
                        else: 
                            LineData.objects.create(from_bus = line_df[1][i],to_bus = line_df[0][i],R = line_df[2][i],X = line_df[3][i],B = line_df[4][i],line_type=line_df[5][i])
                    else:
                        LineData.objects.create(from_bus = line_df[0][i],to_bus = line_df[1][i],R = line_df[2][i],X = line_df[3][i],B = line_df[4][i],line_type=line_df[5][i])
            conditionCheck.objects.create(is_flow=is_flow,is_not_symmetry=is_not_symmetry,find_con=True)
        except:
            e_num = errorcheck.objects.get(find_check=True)
            e_num.errornum = 5
            e_num.save()
            return render(request,'cal/file.html',context={'errornum':e_num})
        e_num = errorcheck.objects.get(find_check=True)
        e_num.errornum = 0
        e_num.save()
        return redirect('condition')
    e_num = errorcheck.objects.get(find_check=True)
    return render(request,'cal/file.html',context={'errornum':e_num})


def fault_con(request):
    clear = FaultCondition.objects.all()
    clear.delete()
    clear = FaultBusData.objects.all()
    clear.delete()
    clear = FaultLineData.objects.all()
    clear.delete()
    clear = ThreeFaultI.objects.all()
    clear.delete()
    clear = ThreeFaultV.objects.all()
    clear.delete()
    clear = OtherFaultI.objects.all()
    clear.delete()
    clear = OtherFaultV.objects.all()
    clear.delete()
    clear = ThreeZbus.objects.all()
    clear.delete()
    clear = OtherZbus.objects.all()
    clear.delete()
    clear = OthersequenceV.objects.all()
    clear.delete()
    clear = OthersequenceI.objects.all()
    clear.delete()
    clear = Afterflow.objects.all()
    clear.delete()
    clear = Sliderbus.objects.all()
    clear.delete()
    clear = SliderLine.objects.all()
    clear.delete()
    if request.method == 'POST':
        basemva = request.POST['basemva']
        is_flow = request.POST['is_flow']
        fault_type = request.POST['fault_type']
        is_bus_fault = request.POST['is_bus_fault']
        fault_bus = request.POST.get('fault_bus',0)
        fault_line_id = request.POST.get('fault_line',0)
        if fault_bus == '-1' or fault_line_id == '-1':
            e_num = errorcheck.objects.get(find_check=True)
            e_num.errornum = 1
            e_num.save()
            return redirect('condition')
        if is_bus_fault == 'False' and fault_line_id == 0:
            return redirect('condition')
        if fault_line_id != 0:
            fault_line = LineData.objects.get(id=fault_line_id)
            fault_line_1 = fault_line.from_bus
            fault_line_2 = fault_line.to_bus
        else:
            fault_line_1 = 0
            fault_line_2 = 0
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
            is_load_effect = is_load_effect,
            to_find = True,
        )
        new_con.save()
        #condition
        j = complex(0, 1)
        isexample = isExample.objects.get(find_ex=True)
        if isexample.isex:
            if isexample.exampleNumber==1:
                file = "/home/jin/fault_calculation_site/fault/media/example/Glover_9.8.xlsx"
            elif isexample.exampleNumber==2:
                file = "/home/jin/fault_calculation_site/fault/media/example/Saadat9.8.xlsx"
            elif isexample.exampleNumber==3:
                file = "/home/jin/fault_calculation_site/fault/media/example/Saadat10.7.xlsx"
            elif isexample.exampleNumber==4:
                file = "/home/jin/fault_calculation_site/fault/media/example/Saadat9.9-1.xlsx"
            elif isexample.exampleNumber==5:
                file = "/home/jin/fault_calculation_site/fault/media/example/Saadat9.9-2.xlsx"
            elif isexample.exampleNumber==6:
                file = "/home/jin/fault_calculation_site/fault/media/example/Saadat10.8.xlsx"
            elif isexample.exampleNumber==7:
                file = "/home/jin/fault_calculation_site/fault/media/example/contest.xlsx"
            bus_df = pd.read_excel(file,sheet_name=0, header=None) 
            line_df = pd.read_excel(file,sheet_name=1, header=None) 
        else:
            file = ExcelFile.objects.get(find_file=True)
            bus_df = pd.read_excel(file.file.path,sheet_name=0, header=None) 
            line_df = pd.read_excel(file.file.path,sheet_name=1, header=None) 
        #file load
        condition = conditionCheck.objects.get(find_con = True)
        fault_con = FaultCondition.objects.get(to_find=True)
        if condition.is_flow:
            try:
                bus_df = bus_scaling(bus_df, fault_con.basemva)
                if fault_con.is_flow:
                    bus_df, repeat_count = gauss_flow(line_df, bus_df)
                    for i in range(len(bus_df)):
                        Afterflow.objects.create(Bus_No=bus_df[0][i],Voltage_Mag=bus_df[1][i],Voltage_Deg=bus_df[2][i],
                                                Generator_MW=bus_df[3][i]*fault_con.basemva, Generator_Mvar=bus_df[4][i]*fault_con.basemva,
                                                Load_MW=bus_df[5][i]*fault_con.basemva,Load_Mvar=bus_df[6][i]*fault_con.basemva)
            except:
                e_num = errorcheck.objects.get(find_check=True)
                e_num.errornum = 2
                e_num.save()
                return redirect('condition')

        try:
            initial_bus_voltage = bus_df.iloc[:, 1] * np.exp(j * np.deg2rad(bus_df.iloc[:, 2]))
            
            fault_impedence = fault_con.impedence_R + j * fault_con.impedence_X

            if fault_con.is_bus_fault:
                fault_loc = fault_con.fault_bus
            else:
                line_df, bus_df, initial_bus_voltage, fault_loc = \
                    line_sliding_scaling(line_df,bus_df, initial_bus_voltage, fault_con.fault_line_1, fault_con.fault_line_2,
                                        fault_con.line_percentage/100, condition.is_flow, condition.is_not_symmetry)
                if condition.is_flow:
                    for i in range(len(bus_df)):
                        Sliderbus.objects.create(Bus_No=bus_df[0][i],Voltage_Mag=bus_df[1][i],Voltage_Deg=bus_df[2][i],
                                                Generator_MW=bus_df[3][i]*fault_con.basemva, Generator_Mvar=bus_df[4][i]*fault_con.basemva,
                                                Load_MW=bus_df[5][i]*fault_con.basemva,Load_Mvar=bus_df[6][i]*fault_con.basemva)
                else:
                    for i in range(len(bus_df)):
                        Sliderbus.objects.create(Bus_No=bus_df[0][i],Voltage_Mag=bus_df[1][i],Voltage_Deg=bus_df[2][i])
                if condition.is_not_symmetry:
                    for i in range(len(line_df)):
                        if line_df[0][i]==0:
                            if line_df[11][i] == 4:
                                SliderLine.objects.create(From_bus = line_df[1][i],To_bus = line_df[0][i],R = line_df[2][i],X = line_df[3][i],
                                                B = line_df[4][i],negative_R = line_df[5][i],negative_X = line_df[6][i],zero_R = line_df[7][i],
                                                zero_X = line_df[8][i],Xn = line_df[9][i],zero_B = line_df[10][i],line_type = 3)
                            else:
                                SliderLine.objects.create(From_bus = line_df[1][i],To_bus = line_df[0][i],R = line_df[2][i],X = line_df[3][i],
                                                B = line_df[4][i],negative_R = line_df[5][i],negative_X = line_df[6][i],zero_R = line_df[7][i],
                                                zero_X = line_df[8][i],Xn = line_df[9][i],zero_B = line_df[10][i],line_type = line_df[11][i])
                        else:
                            SliderLine.objects.create(From_bus = line_df[0][i],To_bus = line_df[1][i],R = line_df[2][i],X = line_df[3][i],
                                                B = line_df[4][i],negative_R = line_df[5][i],negative_X = line_df[6][i],zero_R = line_df[7][i],
                                                zero_X = line_df[8][i],Xn = line_df[9][i],zero_B = line_df[10][i],line_type = line_df[11][i])
                else:
                    for i in range(len(line_df)):
                        if line_df[0][i] ==0:
                            if line_df[5][i]==4:
                                SliderLine.objects.create(From_bus = line_df[1][i],To_bus = line_df[0][i],R = line_df[2][i],X = line_df[3][i],B = line_df[4][i], line_type=3)
                            else:
                                SliderLine.objects.create(From_bus = line_df[1][i],To_bus = line_df[0][i],R = line_df[2][i],X = line_df[3][i],B = line_df[4][i],line_type= line_df[5][i])
                        else:
                            SliderLine.objects.create(From_bus = line_df[0][i],To_bus = line_df[1][i],R = line_df[2][i],X = line_df[3][i],B = line_df[4][i], line_type = line_df[5][i])
            
            if fault_con.fault_type > 0: 
                line_df = fault_line_data_scaling(line_df) 

            if fault_con.fault_type == 0:
                result_v, result_cur, threebus, tybus = three_phase_fault(initial_bus_voltage, line_df, bus_df, fault_loc, fault_impedence,
                                                                    fault_con.is_shunt, fault_con.is_load_effect)
            else:
                result_v, result_cur, bus, negativebus, zerobus, pybus, nybus, zybus, sequencev, sequencei = unbalanced_fault(initial_bus_voltage, line_df, bus_df, fault_loc, fault_impedence,
                                                                    fault_con.fault_type,fault_con.is_shunt, fault_con.is_load_effect)
            result_v, result_cur = after_fault_scaling(line_df, bus_df, result_v, result_cur, fault_loc, fault_con.fault_type, condition.is_not_symmetry)
            if fault_con.fault_type > 0:
                sequencev,sequencei = after_fault_scaling(line_df, bus_df, sequencev, sequencei, fault_loc, fault_con.fault_type, condition.is_not_symmetry)
            if condition.is_flow:
                bus_df = after_flow_scaling(bus_df, fault_con.basemva)
            for i in range(len(bus_df)):
                if condition.is_flow:
                    FaultBusData.objects.create(Bus_No=bus_df[0][i], Voltage_Mag=bus_df[1][i], Voltage_Deg=bus_df[2][i],
                                            Generator_MW=bus_df[3][i],Generator_Mvar=bus_df[4][i],Load_MW=bus_df[5][i],Load_Mvar=bus_df[6][i])
                else:
                    FaultBusData.objects.create(Bus_No=bus_df[0][i], Voltage_Mag=bus_df[1][i], Voltage_Deg=bus_df[2][i])

            for i in range(len(line_df)):
                if condition.is_not_symmetry:
                    if line_df[0][i]==0:
                        if line_df[11][i]==4:
                            FaultLineData.objects.create(From_Bus=line_df[1][i], To_Bus=line_df[0][i], R=line_df[2][i], X=line_df[3][i],
                                            B=line_df[4][i],negative_R=line_df[5][i],negative_X=line_df[6][i],
                                            zero_R=line_df[7][i],zero_X=line_df[8][i],zero_B=line_df[10][i],line_type=3)
                        else:
                            FaultLineData.objects.create(From_Bus=line_df[1][i], To_Bus=line_df[0][i], R=line_df[2][i], X=line_df[3][i],
                                            B=line_df[4][i],negative_R=line_df[5][i],negative_X=line_df[6][i],
                                            zero_R=line_df[7][i],zero_X=line_df[8][i],zero_B=line_df[10][i],line_type=line_df[11][i])
                    else:
                        FaultLineData.objects.create(From_Bus=line_df[0][i], To_Bus=line_df[1][i], R=line_df[2][i], X=line_df[3][i],
                                            B=line_df[4][i],negative_R=line_df[5][i],negative_X=line_df[6][i],
                                            zero_R=line_df[7][i],zero_X=line_df[8][i],zero_B=line_df[10][i],line_type=line_df[11][i])
                else:
                    if line_df[0][i]==0:
                        FaultLineData.objects.create(From_Bus=line_df[1][i], To_Bus=line_df[0][i], R=line_df[2][i], X=line_df[3][i], B=line_df[4][i],line_type=line_df[5][i])
                    else:
                        FaultLineData.objects.create(From_Bus=line_df[0][i], To_Bus=line_df[1][i], R=line_df[2][i], X=line_df[3][i], B=line_df[4][i],line_type=line_df[5][i])
            
            if fault_con.fault_type == 0:
                for i in range(len(result_v)):
                    ThreeFaultV.objects.create(Bus_No=result_v[0][i], Voltage_Mag=result_v[1][i], Voltage_Deg=result_v[2][i])
                for i in range(len(result_cur)):
                    if(result_cur[0][i]==0):
                        if result_cur[4][i]==4:
                            ThreeFaultI.objects.create(From_Bus=result_cur[1][i], To_Bus=result_cur[0][i],
                                                Current_Mag=result_cur[2][i], Current_Deg=result_cur[3][i], line_type = 3)
                        else:
                            ThreeFaultI.objects.create(From_Bus=result_cur[1][i], To_Bus=result_cur[0][i],
                                                Current_Mag=result_cur[2][i], Current_Deg=result_cur[3][i], line_type = result_cur[4][i])
                    else:
                        ThreeFaultI.objects.create(From_Bus=result_cur[0][i], To_Bus=result_cur[1][i],
                                                Current_Mag=result_cur[2][i], Current_Deg=result_cur[3][i], line_type = result_cur[4][i])
                for i in range(len(result_v)):
                    ThreeZbus.objects.create(check = i)
                    row = ThreeZbus.objects.get(check=i)
                    for j in range(len(result_v)):
                        ThreeZbusSource.objects.create(row = row, real_source=threebus[i][j].real, imag_source=threebus[i][j].imag,
                                                        y_real_source = tybus[i][j].real, y_imag_source = tybus[i][j].imag)
            else:
                for i in range(len(result_v)):
                    OtherFaultV.objects.create(Bus_No=result_v[0][i], Phase_A_Mag=result_v[1][i], Phase_A_Deg=result_v[2][i],
                                                Phase_B_Mag=result_v[3][i], Phase_B_Deg=result_v[4][i],Phase_C_Mag=result_v[5][i], Phase_C_Deg=result_v[6][i])
                    OthersequenceV.objects.create(Bus_No=sequencev[0][i], Phase_A_Mag=sequencev[1][i], Phase_A_Deg=sequencev[2][i],
                                                Phase_B_Mag=sequencev[3][i], Phase_B_Deg=sequencev[4][i],Phase_C_Mag=sequencev[5][i], Phase_C_Deg=sequencev[6][i])
                for i in range(len(result_cur)):
                    if(result_cur[0][i]==0):
                        if result_cur[8][i]==4:
                            OtherFaultI.objects.create(From_Bus=result_cur[1][i], To_Bus=result_cur[0][i], Phase_A_Mag=result_cur[2][i], Phase_A_Deg=result_cur[3][i],
                                                    Phase_B_Mag=result_cur[4][i], Phase_B_Deg=result_cur[5][i],Phase_C_Mag=result_cur[6][i], Phase_C_Deg=result_cur[7][i], line_type=3)
                        else:
                            OtherFaultI.objects.create(From_Bus=result_cur[1][i], To_Bus=result_cur[0][i], Phase_A_Mag=result_cur[2][i], Phase_A_Deg=result_cur[3][i],
                                                    Phase_B_Mag=result_cur[4][i], Phase_B_Deg=result_cur[5][i],Phase_C_Mag=result_cur[6][i], Phase_C_Deg=result_cur[7][i], line_type=result_cur[8][i])
                        if sequencei[8][i] == 4:
                            OthersequenceI.objects.create(From_Bus=sequencei[1][i], To_Bus=sequencei[0][i], Phase_A_Mag=sequencei[2][i], Phase_A_Deg=sequencei[3][i],
                                                Phase_B_Mag=sequencei[4][i], Phase_B_Deg=sequencei[5][i],Phase_C_Mag=sequencei[6][i], Phase_C_Deg=sequencei[7][i], line_type=3)
                        else:
                            OthersequenceI.objects.create(From_Bus=sequencei[1][i], To_Bus=sequencei[0][i], Phase_A_Mag=sequencei[2][i], Phase_A_Deg=sequencei[3][i],
                                                Phase_B_Mag=sequencei[4][i], Phase_B_Deg=sequencei[5][i],Phase_C_Mag=sequencei[6][i], Phase_C_Deg=sequencei[7][i], line_type=sequencei[8][i])
                    else:
                        OtherFaultI.objects.create(From_Bus=result_cur[0][i], To_Bus=result_cur[1][i], Phase_A_Mag=result_cur[2][i], Phase_A_Deg=result_cur[3][i],
                                                    Phase_B_Mag=result_cur[4][i], Phase_B_Deg=result_cur[5][i],Phase_C_Mag=result_cur[6][i], Phase_C_Deg=result_cur[7][i], line_type=result_cur[8][i])
                        OthersequenceI.objects.create(From_Bus=sequencei[0][i], To_Bus=sequencei[1][i], Phase_A_Mag=sequencei[2][i], Phase_A_Deg=sequencei[3][i],
                                                Phase_B_Mag=sequencei[4][i], Phase_B_Deg=sequencei[5][i],Phase_C_Mag=sequencei[6][i], Phase_C_Deg=sequencei[7][i], line_type=sequencei[8][i])
                for i in range(len(result_v)):
                    OtherZbus.objects.create(check = i)
                    row = OtherZbus.objects.get(check=i)
                    for j in range(len(result_v)):
                        OtherZbusSource.objects.create(row = row,real_source=bus[i][j].real, imag_source=bus[i][j].imag,
                                                        y_real_source = pybus[i][j].real, y_imag_source = pybus[i][j].imag)
                        negativeZbusSource.objects.create(row = row,real_source=negativebus[i][j].real, imag_source=negativebus[i][j].imag,
                                                            y_real_source = nybus[i][j].real, y_imag_source = nybus[i][j].imag)
                        zeroZbusSource.objects.create(row = row,real_source=zerobus[i][j].real, imag_source=zerobus[i][j].imag,
                                                        y_real_source = zybus[i][j].real, y_imag_source = zybus[i][j].imag)
        except:
            e_num = errorcheck.objects.get(find_check=True)
            e_num.errornum = 3
            e_num.save()
            return redirect('condition')
        return redirect('initial')
    busdata = BusData.objects.all()
    linedata = LineData.objects.filter(line_type=1)
    condition = conditionCheck.objects.get(find_con=True)
    isexample = isExample.objects.get(find_ex=True)
    e_num = errorcheck.objects.get(find_check=True)
    context ={'busdata':busdata,'linedata':linedata,'condition':condition,'isexample':isexample,'errornum':e_num}
    return render(request, 'cal/fault_con.html', context=context)

def result(request):
    busdata = BusData.objects.all()
    linedata = LineData.objects.all().order_by('line_type')
    faultcon = FaultCondition.objects.get(to_find=True)
    faultbusdata=FaultBusData.objects.all()
    faultlinedata=FaultLineData.objects.all().order_by('line_type')
    threefaultv=ThreeFaultV.objects.all()
    threefaulti=ThreeFaultI.objects.all().order_by('line_type')
    otherfaultv=OtherFaultV.objects.all()
    otherfaulti=OtherFaultI.objects.all().order_by('line_type')
    threezbus=ThreeZbus.objects.all()
    threezbussource = ThreeZbusSource.objects.all()
    otherzbus=OtherZbus.objects.all()
    otherzbussource = OtherZbusSource.objects.all()
    negativezbussource = negativeZbusSource.objects.all()
    zerozbussource = zeroZbusSource.objects.all()
    sequencev = OthersequenceV.objects.all()
    sequencei = OthersequenceI.objects.all().order_by('line_type')
    condition = conditionCheck.objects.get(find_con=True)
    clear = resultfile.objects.all()
    clear.delete()
    j = complex(0, 1)
    initial_bus = pd.DataFrame(BusData.objects.all().values()).drop('id', axis=1)
    initial_line = pd.DataFrame(LineData.objects.all().values()).drop('id', axis=1)
    fault_bus = pd.DataFrame(FaultBusData.objects.all().values()).drop('id',axis=1)
    fault_line = pd.DataFrame(FaultLineData.objects.all().values()).drop('id',axis=1)
    if condition.is_flow == False:
        initial_bus.drop(['Generator_MW','Generator_Mvar','Load_MW','Load_Mvar','Qmax','Qmin','Bus_Code'],axis=1,inplace=True)
        fault_bus.drop(['Generator_MW','Generator_Mvar','Load_MW','Load_Mvar'],axis=1,inplace=True)
    if condition.is_not_symmetry == False:
        initial_line.drop(['negative_R','negative_X','zero_R','zero_X','Xn','zero_B'],axis=1,inplace=True)
        fault_line.drop(['negative_R','negative_X','zero_R','zero_X','zero_B'],axis=1,inplace=True)
    bus_size = max(fault_bus.iloc[:,0])
    if faultcon.fault_type==0:
        ybus = np.zeros((bus_size, bus_size), dtype='complex_')
        zbus = np.zeros((bus_size, bus_size), dtype='complex_')
        bus = pd.DataFrame(ThreeZbusSource.objects.all().values())
        z_real = np.round(bus.iloc[:,2],4)
        z_imag = np.round(bus.iloc[:,3],4)
        y_real = np.round(bus.iloc[:,4],4)
        y_imag = np.round(bus.iloc[:,5],4)
        for i in range(bus_size):
            for k in range(bus_size):
                ybus[i][k] = y_real[bus_size*i+k]+j*y_imag[bus_size*i+k]
                zbus[i][k] = z_real[bus_size*i+k]+j*z_imag[bus_size*i+k]
                
        ybus = pd.DataFrame(ybus)
        zbus = pd.DataFrame(zbus)
        threev = pd.DataFrame(ThreeFaultV.objects.all().values()).drop('id',axis=1)
        threei = pd.DataFrame(ThreeFaultI.objects.all().values()).drop('id',axis=1)
        with pd.ExcelWriter('/home/jin/fault_calculation_site/fault/media/result/result.xlsx') as writer:
            initial_bus.to_excel(writer, sheet_name='Initial Voltage Data',index=False)
            initial_line.to_excel(writer, sheet_name='Equipment Data',index=False)
            fault_bus.to_excel(writer, sheet_name='Input Voltage Data',index=False)
            fault_line.to_excel(writer, sheet_name='Impedence Data',index=False)
            ybus.to_excel(writer, sheet_name='Ybus',index=False,header=None)
            zbus.to_excel(writer, sheet_name='Zbus',index=False,header=None)
            threev.to_excel(writer, sheet_name='Fault Voltage',index=False)
            threei.to_excel(writer, sheet_name='Fault Current',index=False)
    else:
        pybus = np.zeros((bus_size, bus_size), dtype='complex_')
        nybus = np.zeros((bus_size, bus_size), dtype='complex_')
        zybus = np.zeros((bus_size, bus_size), dtype='complex_')
        pzbus = np.zeros((bus_size, bus_size), dtype='complex_')
        nzbus = np.zeros((bus_size, bus_size), dtype='complex_')
        zzbus = np.zeros((bus_size, bus_size), dtype='complex_')
        pbus = pd.DataFrame(OtherZbusSource.objects.all().values())
        nbus = pd.DataFrame(negativeZbusSource.objects.all().values())
        zbus = pd.DataFrame(zeroZbusSource.objects.all().values())
        zp_real = np.round(pbus.iloc[:,2],4)
        zp_imag = np.round(pbus.iloc[:,3],4)
        yp_real = np.round(pbus.iloc[:,4],4)
        yp_imag = np.round(pbus.iloc[:,5],4)
        zn_real = np.round(nbus.iloc[:,2],4)
        zn_imag = np.round(nbus.iloc[:,3],4)
        yn_real = np.round(nbus.iloc[:,4],4)
        yn_imag = np.round(nbus.iloc[:,5],4)
        zz_real = np.round(zbus.iloc[:,2],4)
        zz_imag = np.round(zbus.iloc[:,3],4)
        yz_real = np.round(zbus.iloc[:,4],4)
        yz_imag = np.round(zbus.iloc[:,5],4)
        for i in range(bus_size):
            for k in range(bus_size):
                pybus[i][k] = yp_real[bus_size*i+k]+j*yp_imag[bus_size*i+k]
                pzbus[i][k] = zp_real[bus_size*i+k]+j*zp_imag[bus_size*i+k]
                nybus[i][k] = yn_real[bus_size*i+k]+j*yn_imag[bus_size*i+k]
                nzbus[i][k] = zn_real[bus_size*i+k]+j*zn_imag[bus_size*i+k]
                zybus[i][k] = yz_real[bus_size*i+k]+j*yz_imag[bus_size*i+k]
                zzbus[i][k] = zz_real[bus_size*i+k]+j*zz_imag[bus_size*i+k]
                
        pybus = pd.DataFrame(pybus)
        pzbus = pd.DataFrame(pzbus)
        nybus = pd.DataFrame(nybus)
        nzbus = pd.DataFrame(nzbus)
        zybus = pd.DataFrame(zybus)
        zzbus = pd.DataFrame(zzbus)
        sequence_v = pd.DataFrame(OthersequenceV.objects.all().values()).drop('id',axis=1)
        sequence_i = pd.DataFrame(OthersequenceI.objects.all().values()).drop('id',axis=1)
        otherv = pd.DataFrame(OtherFaultV.objects.all().values()).drop('id',axis=1)
        otheri = pd.DataFrame(OtherFaultI.objects.all().values()).drop('id',axis=1)
        with pd.ExcelWriter('/home/jin/fault_calculation_site/fault/media/result/result.xlsx') as writer:
            initial_bus.to_excel(writer, sheet_name='Initial Voltage Data',index=False)
            initial_line.to_excel(writer, sheet_name='Equipment Data',index=False)
            fault_bus.to_excel(writer, sheet_name='Input Voltage Data',index=False)
            fault_line.to_excel(writer, sheet_name='Impedence Data',index=False)
            pybus.to_excel(writer, sheet_name='Positive Ybus',index=False,header=None)
            nybus.to_excel(writer, sheet_name='Negative Ybus',index=False,header=None)
            zybus.to_excel(writer, sheet_name='Zero Ybus',index=False,header=None)
            pzbus.to_excel(writer, sheet_name='Positive Zbus',index=False,header=None)
            nzbus.to_excel(writer, sheet_name='Negative Zbus',index=False,header=None)
            zzbus.to_excel(writer, sheet_name='Zero Zbus',index=False,header=None)
            sequence_v.to_excel(writer, sheet_name='Fault Sequence Voltage',index=False)
            sequence_i.to_excel(writer, sheet_name='Fault Sequence Current',index=False) 
            otherv.to_excel(writer, sheet_name='Fault Phase Voltage',index=False)
            otheri.to_excel(writer, sheet_name='Fault Phase Current',index=False)
    resultfile.objects.create(find_file=True)
    outfile = resultfile.objects.get(find_file=True)
    path = Path('/home/jin/fault_calculation_site/fault/media/result/result.xlsx')
    with path.open(mode='rb') as f:
        outfile.rfile = File(f, name=path.name)
        outfile.save()
    context = {'faultbusdata':faultbusdata,'faultlinedata':faultlinedata,'threefaultv':threefaultv,'threefaulti':threefaulti,
                'otherfaultv':otherfaultv,'otherfaulti':otherfaulti, 'faultcon':faultcon,'threezbus':threezbus,
                'tsource':threezbussource,'otherzbus':otherzbus,'osource':otherzbussource,'nsource':negativezbussource,
                'zsource':zerozbussource,'condition':condition,'busdata':busdata,'linedata':linedata,'sequencev':sequencev,
                'sequencei':sequencei,'outfile':outfile}
    return render(request, 'cal/fault_result.html',context=context)

def initial(request):
    faultcon = FaultCondition.objects.get(to_find=True)
    busdata = BusData.objects.all()
    linedata = LineData.objects.all().order_by('line_type')
    condition = conditionCheck.objects.get(find_con=True)
    context ={'busdata':busdata,'linedata':linedata,'condition':condition,'faultcon':faultcon}
    return render(request, 'cal/initial_circuit.html', context=context)

def flow(request):
    afterflow=Afterflow.objects.all()
    fault_con = FaultCondition.objects.get(to_find=True)
    context={'afterflow':afterflow, 'fault_con':fault_con}
    return render(request,'cal/flow.html',context=context)

def slider(request):
    sliderbus = Sliderbus.objects.all()
    sliderline = SliderLine.objects.all().order_by('line_type')
    condition = conditionCheck.objects.get(find_con=True)
    fault_con = FaultCondition.objects.get(to_find=True)
    context={'sliderbus':sliderbus, 'sliderline':sliderline,'fault_con':fault_con,'condition':condition}
    return render(request,'cal/slider.html',context=context)

def transformer(request):
    faultlinedata=FaultLineData.objects.all().order_by('line_type')
    faultcon = FaultCondition.objects.get(to_find=True)
    return render(request,'cal/transformer.html',context={'faultlinedata':faultlinedata,'faultcon':faultcon})

def show_zbus(request):
    faultcon = FaultCondition.objects.get(to_find=True)
    threezbus=ThreeZbus.objects.all()
    threezbussource = ThreeZbusSource.objects.all()
    otherzbus=OtherZbus.objects.all()
    otherzbussource = OtherZbusSource.objects.all()
    negativezbussource = negativeZbusSource.objects.all()
    zerozbussource = zeroZbusSource.objects.all()
    context={'threezbus':threezbus,'tsource':threezbussource,'otherzbus':otherzbus,'osource':otherzbussource,'nsource':negativezbussource,
                'zsource':zerozbussource, 'faultcon':faultcon}
    return render(request, 'cal/zbus.html',context=context)

def show_ybus(request):
    faultcon = FaultCondition.objects.get(to_find=True)
    threezbus=ThreeZbus.objects.all()
    threezbussource = ThreeZbusSource.objects.all()
    otherzbus=OtherZbus.objects.all()
    otherzbussource = OtherZbusSource.objects.all()
    negativezbussource = negativeZbusSource.objects.all()
    zerozbussource = zeroZbusSource.objects.all()
    context={'threezbus':threezbus,'tsource':threezbussource,'otherzbus':otherzbus,'osource':otherzbussource,'nsource':negativezbussource,
                'zsource':zerozbussource, 'faultcon':faultcon}
    return render(request, 'cal/ybus.html',context=context)

def sequence(request):
    sequencev = OthersequenceV.objects.all()
    sequencei = OthersequenceI.objects.all().order_by('line_type')
    return render(request, 'cal/sequence.html',context={'sequencev':sequencev,'sequencei':sequencei})

def phase(request):
    faultcon = FaultCondition.objects.get(to_find=True)
    threefaultv=ThreeFaultV.objects.all()
    threefaulti=ThreeFaultI.objects.all().order_by('line_type')
    otherfaultv=OtherFaultV.objects.all()
    otherfaulti=OtherFaultI.objects.all().order_by('line_type')
    context={'threefaultv':threefaultv,'threefaulti':threefaulti,'otherfaultv':otherfaultv,'otherfaulti':otherfaulti,'faultcon':faultcon}
    return render(request, 'cal/phase.html',context=context)

def reference(request):
    return render(request, 'cal/reference.html')

def bus_scaling(bus_df, basemva):
    bus_df.iloc[:, 3:9] /= basemva
    return bus_df

def flow_y_bus(line_d):
    j = complex(0, 1)
    fb = line_d.iloc[:, 0]
    tb = line_d.iloc[:, 1]
    r = line_d.iloc[:, 2]
    x = line_d.iloc[:, 3]
    b = j * line_d.iloc[:, 4]
    bus_size = max(max(fb), max(tb))
    con_num = len(fb)
    z = r + j * x
    y = np.ones(con_num, dtype='complex_')
    for i in range(con_num):
        if z[i] == 0:
            y[i] = 0
        else:
            y[i] /= z[i]
    bus = np.zeros((bus_size, bus_size), dtype='complex_')
    for i in range(con_num):
        if fb[i] == 0:
            continue
        elif tb[i] == 0:
            continue
        else:
            bus[fb[i] - 1, tb[i] - 1] -= y[i]
            bus[tb[i] - 1, fb[i] - 1] -= y[i]
            bus[fb[i] - 1, fb[i] - 1] += y[i] + b[i]/2
            bus[tb[i] - 1, tb[i] - 1] += y[i] + b[i]/2
    return bus

def gauss_flow(line_d, bus_d):
    flow_bus = flow_y_bus(line_d)
    j = complex(0, 1)
    bus_n = bus_d.iloc[:, 0]  # bus number
    init_v_mag = bus_d.iloc[:, 1]  # init_voltage_magnitude
    init_v_deg = bus_d.iloc[:, 2]  # init_voltage_degree
    p_gen = bus_d.iloc[:, 3]  # active_power_generator
    q_gen = bus_d.iloc[:, 4]  # reactive_power_generator
    p_load = bus_d.iloc[:, 5]  # active_power_load
    q_load = bus_d.iloc[:, 6]  # reactive_power_load
    q_max = bus_d.iloc[:, 7]
    q_min = bus_d.iloc[:, 8]
    bus_ty = bus_d.iloc[:, 9]  # bus type
    bus_size = max(bus_n)
    p_power = p_gen - p_load
    q_power = q_gen - q_load
    prev_v = init_v_mag * np.exp(j * np.deg2rad(init_v_deg))
    curr_v = init_v_mag * np.exp(j * np.deg2rad(init_v_deg))
    error = 1
    repeat = 0
    code_change = np.zeros(bus_size)
    while error > math.pow(10, -7) and repeat <= 1000:
        repeat += 1
        for i in range(bus_size):
            cal_sum = 0
            pv_cal_sum = 0
            if bus_ty[i] == 1:
                continue
            for k in range(bus_size):
                if i != k:
                    cal_sum += flow_bus[k, i] * curr_v[k]
                    pv_cal_sum -= flow_bus[k, i]
            if bus_ty[i] == 3 and code_change[i] == 0:
                q_power[i] = -(curr_v[i].conjugate() * (curr_v[i] * pv_cal_sum + cal_sum)).imag
                if q_max[i] != 0 and repeat > 20:
                    if q_power[i] > q_max[i]:
                        q_power[i] = q_max[i]
                        code_change[i] = 1
                    elif q_power[i] < q_min[i]:
                        q_power[i] = q_min[i]
                        code_change[i] = 1
            curr_v[i] = ((p_power[i] - j * q_power[i]) / curr_v[i].conjugate() - cal_sum) / flow_bus[i, i]
            if bus_ty[i] == 3 and code_change[i] == 0:
                real_v = math.sqrt(math.pow(init_v_mag[i], 2) - math.pow(curr_v[i].imag, 2))
                curr_v[i] = real_v + j * curr_v[i].imag
            if code_change[i] == 1 and abs(curr_v[i] - prev_v[i]) < math.pow(10, -4):
                if q_power[i] == q_max[i] and abs(curr_v[i]) < init_v_mag[i]:
                    code_change[i] = 0
                    real_v = math.sqrt(math.pow(init_v_mag[i], 2) - math.pow(curr_v[i].imag, 2))
                    curr_v[i] = real_v + j * curr_v[i].imag
                elif q_power[i] == q_min[i] and abs(curr_v[i]) > init_v_mag[i]:
                    code_change[i] = 0
                    real_v = math.sqrt(math.pow(init_v_mag[i], 2) - math.pow(curr_v[i].imag, 2))
                    curr_v[i] = real_v + j * curr_v[i].imag
        error = max(abs(curr_v - prev_v))
        prev_v = curr_v.copy()
    bus_d.iloc[:, 1] = np.abs(curr_v)
    bus_d.iloc[:, 2] = np.angle(curr_v, deg=True)
    bus_d.iloc[:, 4] = q_power + q_load
    return bus_d, repeat

def fault_line_data_scaling(line_df):
    fb = line_df.iloc[:, 0]
    con_num = len(fb)
    line_df.iloc[:,8] += 3 * line_df.iloc[:, 9]
    append_count = 0
    for i in range(con_num):
        if line_df[11][i] == 3:
            line_df.loc[con_num + append_count] = [line_df[0][i], 0, 0, 0, line_df[4][i], 0, 0,
                                                    line_df[7][i], line_df[8][i], line_df[9][i],
                                                    line_df[10][i], line_df[11][i]]
            append_count += 1
            line_df[7][i] = 0
            line_df[8][i] = 0
            line_df[9][i] = 0
        if line_df[11][i] == 4:
            line_df.loc[con_num + append_count] = [0, line_df[1][i], 0, 0, line_df[4][i], 0, 0,
                                                    line_df[7][i], line_df[8][i], line_df[9][i],
                                                    line_df[10][i], line_df[11][i]]
            append_count += 1
            line_df[7][i] = 0
            line_df[8][i] = 0
            line_df[9][i] = 0
        if line_df[11][i] >= 5:
            line_df[7][i] = 0
            line_df[8][i] = 0
            line_df[9][i] = 0
    line_df = line_df.astype({0: 'int'})
    line_df = line_df.astype({1: 'int'})
    return line_df

def line_sliding_scaling(line_d,bus_d, voltage, fault_bus_1, fault_bus_2, percent, is_flow, is_not_sym):
    fb = line_d.iloc[:, 0]
    tb = line_d.iloc[:, 1]
    con_num = len(fb)
    bus_size = max(max(fb), max(tb))
    if is_not_sym:
        for i in range(con_num):
            if (fb[i] == fault_bus_1 and tb[i] == fault_bus_2) or (tb[i] == fault_bus_1 and fb[i] == fault_bus_2):
                temp_line = line_d.loc[i, :]
                if temp_line[0] == fault_bus_1:
                    line_d.loc[i] = [temp_line[0], bus_size + 1, temp_line[2] * percent,
                                    temp_line[3] * percent, temp_line[4] * percent,
                                    temp_line[5] * percent, temp_line[6] * percent,
                                    temp_line[7] * percent, temp_line[8] * percent,
                                    temp_line[9] * percent, temp_line[10] * percent,
                                    temp_line[11]]
                    line_d.loc[con_num] = [bus_size + 1, temp_line[1], temp_line[2] * (1-percent),
                                        temp_line[3] * (1-percent), temp_line[4] * (1-percent),
                                        temp_line[5] * (1-percent), temp_line[6] * (1-percent),
                                        temp_line[7] * (1-percent), temp_line[8] * (1-percent),
                                        temp_line[9] * (1-percent), temp_line[10] * (1-percent),
                                        temp_line[11]]
                    break
                else:
                    line_d.loc[i] = [bus_size + 1, temp_line[1], temp_line[2] * percent,
                                    temp_line[3] * percent, temp_line[4] * percent,
                                    temp_line[5] * percent, temp_line[6] * percent,
                                    temp_line[7] * percent, temp_line[8] * percent,
                                    temp_line[9] * percent, temp_line[10] * percent,
                                    temp_line[11]]
                    line_d.loc[con_num] = [temp_line[0], bus_size + 1, temp_line[2] * (1-percent),
                                        temp_line[3] * (1-percent), temp_line[4] * (1-percent),
                                        temp_line[5] * (1-percent), temp_line[6] * (1-percent),
                                        temp_line[7] * (1-percent), temp_line[8] * (1-percent),
                                        temp_line[9] * (1-percent), temp_line[10] * (1-percent),
                                        temp_line[11]]
                    break
    else:
        for i in range(con_num):
            if (fb[i] == fault_bus_1 and tb[i] == fault_bus_2) or (tb[i] == fault_bus_1 and fb[i] == fault_bus_2):
                temp_line = line_d.loc[i, :]
                if temp_line[0] == fault_bus_1:
                    line_d.loc[i] = [temp_line[0], bus_size + 1, temp_line[2] * percent,
                                    temp_line[3] * percent, temp_line[4] * percent, 1]
                    line_d.loc[con_num] = [bus_size + 1, temp_line[1], temp_line[2] * (1-percent),
                                        temp_line[3] * (1-percent), temp_line[4] * (1-percent), 1]
                    break
                else:
                    line_d.loc[i] = [bus_size + 1, temp_line[1], temp_line[2] * percent,
                                    temp_line[3] * percent, temp_line[4] * percent, 1]
                    line_d.loc[con_num] = [temp_line[0], bus_size + 1, temp_line[2] * (1-percent),
                                        temp_line[3] * (1-percent), temp_line[4] * (1-percent), 1]
                    break
    voltage.loc[bus_size] = voltage[fault_bus_1 - 1] * percent + voltage[fault_bus_2 - 1] * (1-percent)
    if is_flow:
        bus_d.loc[bus_size] = [bus_size+1,np.abs(voltage.loc[bus_size]), np.angle(voltage.loc[bus_size],deg=True),0,0,0,0,0,0,1]
    else:
        bus_d.loc[bus_size] = [bus_size+1,np.abs(voltage.loc[bus_size]),np.angle(voltage.loc[bus_size],deg=True)]
    fault_loc = bus_size + 1
    bus_d = bus_d.astype({0: 'int'})
    line_d = line_d.astype({0: 'int'})
    line_d = line_d.astype({1: 'int'})
    return line_d, bus_d, voltage, fault_loc

def y_bus(line_d):
    j = complex(0, 1)
    fb = line_d.iloc[:, 0]
    tb = line_d.iloc[:, 1]
    r = line_d.iloc[:, 2]
    x = line_d.iloc[:, 3]
    b = j * line_d.iloc[:, 4]
    bus_size = max(max(fb), max(tb))
    con_num = len(fb)  # condition number
    z = r + j * x
    y = np.ones(con_num, dtype='complex_')
    for i in range(con_num):
        if z[i] == 0:
            y[i] = 0
        else:
            y[i] /= z[i]
    bus = np.zeros((bus_size, bus_size), dtype='complex_')
    for i in range(con_num):
        if fb[i] == 0:
            bus[tb[i] - 1, tb[i] - 1] += y[i]
        elif tb[i] == 0:
            bus[fb[i] - 1, fb[i] - 1] += y[i]
        else:
            bus[fb[i] - 1, tb[i] - 1] -= y[i]
            bus[tb[i] - 1, fb[i] - 1] -= y[i]
            bus[fb[i] - 1, fb[i] - 1] += y[i] + b[i]/2
            bus[tb[i] - 1, tb[i] - 1] += y[i] + b[i]/2
    return bus


def zbus(line_d):
    return np.linalg.inv(y_bus(line_d)), y_bus(line_d)


def load_zbus(line_d, bus_d):
    j = complex(0, 1)
    bus = y_bus(line_d)
    bus_n = bus_d.iloc[:, 0]
    v_mag = bus_d.iloc[:, 1]
    p_load = bus_d.iloc[:, 5]
    q_load = bus_d.iloc[:, 6]
    conj_s_load = p_load - j * q_load
    bus_size = max(bus_n)
    for i in range(bus_size):
        if conj_s_load[i] == 0:
            continue
        else:
            bus[i, i] += conj_s_load[i] / (v_mag[i]*v_mag[i])
    return np.linalg.inv(bus), bus


def three_phase_fault(bus_voltage, line_d, bus_d, fault_location, fault_impedance,
                        b_consider, is_bus_load):
    j = complex(0, 1)
    fb = line_d.iloc[:, 0]
    tb = line_d.iloc[:, 1]
    r = line_d.iloc[:, 2]
    x = line_d.iloc[:, 3]
    b = line_d.iloc[:, 4]

    if not b_consider:
        b *= 0

    three_phase_d = pd.concat([fb, tb, r, x, b], axis=1)
    z = r + j * x
    con_num = len(fb)
    bus_size = max(max(fb), max(tb))
    if is_bus_load:
        fault_bus, ybus = load_zbus(three_phase_d, bus_d)
    else:
        fault_bus, ybus = zbus(three_phase_d)
    fl = fault_location - 1
    fault_current = bus_voltage[fl] / (fault_impedance + fault_bus[fl][fl])
    fault_bus_voltage = bus_voltage.copy()
    for i in range(bus_size):
        fault_bus_voltage[i] -= bus_voltage[i] * \
                                fault_bus[i][fl]/(fault_impedance + fault_bus[fl][fl])
    fault_line_current = np.zeros((con_num + 1, 1), dtype='complex_')
    for i in range(con_num):
        if fb[i] == 0:
            fault_line_current[i] = (bus_voltage[tb[i] - 1] - fault_bus_voltage[tb[i] - 1]) / z[i]
        elif tb[i] == 0:
            fault_line_current[i] = (bus_voltage[fb[i] - 1] - fault_bus_voltage[fb[i] - 1]) / z[i]
        else:
            fault_line_current[i] = (fault_bus_voltage[fb[i] - 1] - fault_bus_voltage[tb[i] - 1]) / z[i]
    fault_line_current[con_num] = fault_current
    return fault_bus_voltage, fault_line_current, fault_bus, ybus


def unbalanced_fault(bus_voltage, line_d, bus_d, fault_location, fault_impedance, fault_type,
                    b_consider, is_bus_load):
    j = complex(0, 1)
    fb = line_d.iloc[:, 0]
    tb = line_d.iloc[:, 1]
    positive_r = line_d.iloc[:, 2]
    positive_x = line_d.iloc[:, 3]
    b = line_d.iloc[:, 4]
    negative_r = line_d.iloc[:, 5]
    negative_x = line_d.iloc[:, 6]
    zero_r = line_d.iloc[:, 7]
    zero_x = line_d.iloc[:, 8]
    zero_b = line_d.iloc[:, 10]

    con_num = len(fb)
    bus_size = max(max(fb), max(tb))

    positive_z = positive_r + j * positive_x
    negative_z = negative_r + j * negative_x
    zero_z = zero_r + j * zero_x

    if not b_consider:
        b *= 0
    if is_bus_load:
        positive_fault_bus, pybus = df_to_load_zbus(fb, tb, positive_r, positive_x, b, bus_d)
        negative_fault_bus, nybus = df_to_load_zbus(fb, tb, negative_r, negative_x, b, bus_d)
        zero_fault_bus, zybus = df_to_load_zbus(fb, tb, zero_r, zero_x, zero_b, bus_d)
    else:
        positive_fault_bus, pybus = df_to_zbus(fb, tb, positive_r, positive_x, b)
        negative_fault_bus, nybus = df_to_zbus(fb, tb, negative_r, negative_x, b)
        zero_fault_bus, zybus = df_to_zbus(fb, tb, zero_r, zero_x, zero_b)
    fl = fault_location - 1
    a_matrix = symmetrical_components_transformation_matrix()

    fault_current = fault_current_calculation(fault_type, bus_voltage, fl, positive_fault_bus,
                                                        negative_fault_bus, zero_fault_bus, fault_impedance)
    fault_phase_current = a_matrix @ fault_current

    symmetrical_fault_bus_voltage = np.zeros((bus_size, 3), dtype='complex_')
    fault_bus_voltage = np.zeros((bus_size, 3), dtype='complex_')
    symmetrical_components = np.zeros((3, 1), dtype='complex_')
    for i in range(bus_size):
        symmetrical_components[0] = - zero_fault_bus[i][fl] * fault_current[0]
        symmetrical_components[1] = bus_voltage[i] - positive_fault_bus[i][fl] * fault_current[1]
        symmetrical_components[2] = - negative_fault_bus[i][fl] * fault_current[2]
        symmetrical_fault_bus_voltage[i][:] = np.transpose(symmetrical_components)
        fault_bus_voltage[i, :] = np.transpose(a_matrix @ symmetrical_components)

    fault_line_current = np.zeros((con_num + 1, 3), dtype='complex_')
    symmetrical_fault_line_current = np.zeros((con_num + 1, 3), dtype='complex_')

    for i in range(con_num):
        symmetrical_components = \
            symmetrical_component_fault_current(fb, tb, bus_voltage, symmetrical_fault_bus_voltage,
                                                        positive_z, negative_z, zero_z, i)
        symmetrical_fault_line_current[i][:] = np.transpose(symmetrical_components)
        fault_line_current[i, :] = np.transpose(a_matrix @ symmetrical_components)
    symmetrical_fault_line_current[con_num, :] = np.transpose(fault_current)
    fault_line_current[con_num, :] = np.transpose(fault_phase_current)

    return fault_bus_voltage, fault_line_current, positive_fault_bus, negative_fault_bus, zero_fault_bus, pybus, nybus, zybus, symmetrical_fault_bus_voltage, symmetrical_fault_line_current

def symmetrical_components_transformation_matrix():
    j = complex(0, 1)
    matrix = np.ones((3, 3), dtype='complex_')
    matrix[1][1] = np.exp(j * np.deg2rad(120)) ** 2
    matrix[1][2] = np.exp(j * np.deg2rad(120))
    matrix[2][1] = matrix[1][2]
    matrix[2][2] = matrix[1][1]
    return matrix


def fault_current_calculation(fault_type, bus_v, fl, p_bus, n_bus, z_bus, z_f):
    fault_current = np.zeros((3, 1), dtype='complex_')
    if fault_type == 1:
        fault_current[0] = bus_v[fl] / (p_bus[fl][fl] + n_bus[fl][fl] + z_bus[fl][fl] + 3 * z_f)
        fault_current[1] = fault_current[0]
        fault_current[2] = fault_current[1]
    elif fault_type == 2:
        fault_current[1] = bus_v[fl] / (p_bus[fl][fl] + n_bus[fl][fl] + z_f)
        fault_current[2] = -1 * fault_current[1]
    elif fault_type == 3:
        formula = n_bus[fl][fl] * (z_bus[fl][fl] + 3 * z_f) / (n_bus[fl][fl] + z_bus[fl][fl] + 3 * z_f)
        fault_current[1] = bus_v[fl] / (p_bus[fl][fl] + formula)
        fault_current[2] = - fault_current[1] * formula / n_bus[fl][fl]
        fault_current[0] = - fault_current[1] * formula / (z_bus[fl][fl] + 3 * z_f)
    return fault_current


def df_to_zbus(fb, tb, r, x, b):
    df = pd.concat([fb, tb, r, x, b], axis=1)
    return zbus(df)


def df_to_load_zbus(fb, tb, r, x, b, bus_d):
    df = pd.concat([fb, tb, r, x, b], axis=1)
    return load_zbus(df, bus_d)


def symmetrical_component_fault_current(fb, tb, bus_v, sym_v, p_z, n_z, z_z, i):
    symmetrical_components = np.zeros((3, 1), dtype='complex_')
    if fb[i] == 0:
        symmetrical_components[0] = - sym_v[tb[i] - 1][0] / z_z[i] if z_z[i] != 0 else 0
        symmetrical_components[1] = (bus_v[tb[i] - 1] - sym_v[tb[i] - 1][1]) / p_z[i] if p_z[i] != 0 else 0
        symmetrical_components[2] = - sym_v[tb[i] - 1][2] / n_z[i] if n_z[i] != 0 else 0
    elif tb[i] == 0:
        symmetrical_components[0] = - sym_v[fb[i] - 1][0] / z_z[i] if z_z[i] != 0 else 0
        symmetrical_components[1] = (bus_v[fb[i] - 1] - sym_v[fb[i] - 1][1]) / p_z[i] if p_z[i] != 0 else 0
        symmetrical_components[2] = - sym_v[fb[i] - 1][2] / n_z[i] if n_z[i] != 0 else 0
    else:
        symmetrical_components[0] = (sym_v[fb[i] - 1][0] - sym_v[tb[i] - 1][0]) / z_z[i] if z_z[i] != 0 else 0
        symmetrical_components[1] = (sym_v[fb[i] - 1][1] - sym_v[tb[i] - 1][1]) / p_z[i] if p_z[i] != 0 else 0
        symmetrical_components[2] = (sym_v[fb[i] - 1][2] - sym_v[tb[i] - 1][2]) / n_z[i] if n_z[i] != 0 else 0
    return symmetrical_components

def after_flow_scaling(bus_df, base_mva):
    bus_df.iloc[:, 3:9] *= base_mva
    return bus_df

def after_fault_scaling(line_df, bus_df, voltage_d, current_d, fault_loc, fault_type, is_not_symmetry):
    fb = line_df.iloc[:, 0]
    tb = line_df.iloc[:, 1]
    if is_not_symmetry == True:
        line_type=line_df.iloc[:, 11]
    else:
        line_type=line_df.iloc[:, 5]
    con_num = len(fb)
    current_d = np.round(current_d, 5)
    voltage_d = np.round(voltage_d, 5)
    bus_num = bus_df.iloc[:, 0]
    if fault_type == 0:
        frame_current_mag = pd.DataFrame(np.abs(current_d))
        frame_current_ang = pd.DataFrame(np.angle(current_d, deg=True))
        frame_current_d = pd.concat([fb, tb, frame_current_mag, frame_current_ang, line_type], axis=1)
        frame_voltage_mag = pd.DataFrame(np.abs(voltage_d))
        frame_voltage_ang = pd.DataFrame(np.angle(voltage_d, deg=True))
        frame_voltage_d = pd.concat([bus_num, frame_voltage_mag, frame_voltage_ang], axis=1)
        frame_current_d.columns = [0, 1, 2, 3, 4]
        frame_voltage_d.columns = [0, 1, 2]
        frame_current_d.iloc[con_num, 4] = 8
    else:
        frame_current_mag_a = pd.DataFrame(np.abs(current_d[:, 0]))
        frame_current_ang_a = pd.DataFrame(np.angle(current_d[:, 0], deg=True))
        frame_current_mag_b = pd.DataFrame(np.abs(current_d[:, 1]))
        frame_current_ang_b = pd.DataFrame(np.angle(current_d[:, 1], deg=True))
        frame_current_mag_c = pd.DataFrame(np.abs(current_d[:, 2]))
        frame_current_ang_c = pd.DataFrame(np.angle(current_d[:, 2], deg=True))
        frame_current_d = pd.concat([fb, tb, frame_current_mag_a, frame_current_ang_a, frame_current_mag_b,
                                    frame_current_ang_b, frame_current_mag_c, frame_current_ang_c, line_type], axis=1)
        frame_voltage_mag_a = pd.DataFrame(np.abs(voltage_d[:, 0]))
        frame_voltage_ang_a = pd.DataFrame(np.angle(voltage_d[:, 0], deg=True))
        frame_voltage_mag_b = pd.DataFrame(np.abs(voltage_d[:, 1]))
        frame_voltage_ang_b = pd.DataFrame(np.angle(voltage_d[:, 1], deg=True))
        frame_voltage_mag_c = pd.DataFrame(np.abs(voltage_d[:, 2]))
        frame_voltage_ang_c = pd.DataFrame(np.angle(voltage_d[:, 2], deg=True))
        frame_voltage_d = pd.concat([bus_num, frame_voltage_mag_a, frame_voltage_ang_a, frame_voltage_mag_b,
                                    frame_voltage_ang_b, frame_voltage_mag_c, frame_voltage_ang_c], axis=1)
        frame_current_d.columns = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        frame_voltage_d.columns = [0, 1, 2, 3, 4, 5, 6]
        frame_current_d.iloc[con_num, 8] = 8
    bus_num = frame_voltage_d.iloc[:, 0]
    b_n = len(bus_num)
    frame_voltage_d.iloc[b_n - 1,0] = b_n
    frame_current_d.iloc[con_num, 0] = fault_loc
    frame_current_d.iloc[con_num, 1] = -1
    return frame_voltage_d, frame_current_d
