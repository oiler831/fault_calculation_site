from django.shortcuts import render, redirect
from .models import (FaultCondition, BusData, LineData, ExcelFile,FaultLineData,FaultBusData,
                    ThreeFaultI,ThreeFaultV,OtherFaultI,OtherFaultV)
import pandas as pd
import numpy as np
import math
import sqlite3

# Create your views here.
def index(request):
    return render(request,'cal/main.html')

def manual(request):
    return render(request,'cal/main.html')


def upload_excel_to_db(request):
    if request.method == 'POST':
        clear = BusData.objects.all()
        clear.delete()
        clear = LineData.objects.all()
        clear.delete()
        clear = ExcelFile.objects.all()
        clear.delete()
        excel_file = request.FILES['excelFile']
        find_file = True
        new_file = ExcelFile(file = excel_file, find_file = find_file)
        new_file.save()
        bus_df = pd.read_excel(excel_file,header=None,sheet_name=0)
        line_df = pd.read_excel(excel_file,header=None,sheet_name=1)
        for i in range(len(bus_df)):
            BusData.objects.create(bus_num = bus_df[0][i])
        for i in range(len(line_df)):
            LineData.objects.create(from_bus = line_df[0][i],to_bus = line_df[1][i])
        return redirect('condition')
    return render(request,'cal/main.html')


def fault_con(request):
    if request.method == 'POST':
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
        
        basemva = request.POST['basemva']
        is_flow = request.POST['is_flow']
        fault_type = request.POST['fault_type']
        is_bus_fault = request.POST['is_bus_fault']
        fault_bus = request.POST.get('fault_bus',0)
        fault_line_id = request.POST.get('fault_line',0)
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
        file = ExcelFile.objects.get(find_file=True)
        line_df = pd.read_excel(file.file.path, header=None) 
        # con = sqlite3.connect("/home/jin/graduation/fault/db.sqlite3")
        # line_df.to_sql('test',con,dtype=float)
        # df = pd.read_sql("SELECT * FROM test", con, index_col='index')
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
        j = complex(0, 1)
        file = ExcelFile.objects.get(find_file=True)
        fault_con = FaultCondition.objects.get(to_find=True)
        bus_df = pd.read_excel(file.file.path,sheet_name=0, header=None) 
        line_df = pd.read_excel(file.file.path,sheet_name=1, header=None) 
        bus_df = bus_scaling(bus_df, fault_con.basemva)
        if fault_con.is_flow:
            bus_df, repeat_count = gauss_flow_test(line_df, bus_df)

        initial_bus_voltage = bus_df.iloc[:, 1] * np.exp(j * np.deg2rad(bus_df.iloc[:, 2])) 
        line_df = fault_line_data_scaling(line_df, fault_con.fault_type) 
        
        fault_impedence = fault_con.impedence_R + j * fault_con.impedence_X
        if fault_con.is_bus_fault:
            fault_loc = fault_con.fault_bus
        else:
            line_df, initial_bus_voltage, fault_loc = \
                line_sliding_scaling(line_df, initial_bus_voltage, fault_con.fault_line_1, fault_con.fault_line_2, fault_con.line_percentage/100)
        
        result_v, result_cur = fault_select(initial_bus_voltage, line_df, bus_df,
                                                            fault_loc, fault_impedence, fault_con.fault_type,
                                                            fault_con.is_shunt, fault_con.is_load_effect)
        result_v, result_cur = after_fault_scaling(line_df, bus_df, result_v, result_cur, fault_loc, fault_con.fault_type)
        bus_df = after_flow_scaling(bus_df, fault_con.basemva)
        for i in range(len(bus_df)):
            FaultBusData.objects.create(Bus_No=bus_df[0][i], Bus_Code=bus_df[9][i], Voltage_Mag=bus_df[1][i], Voltage_Deg=bus_df[2][i],
                                        Generator_MW=bus_df[3][i],Generator_Mvar=bus_df[4][i],Load_MW=bus_df[5][i],Load_Mvar=bus_df[6][i])

        for i in range(len(line_df)):
            FaultLineData.objects.create(From_Bus=line_df[0][i], To_Bus=line_df[1][i], R=line_df[2][i], X=line_df[3][i],
                                        half_B=line_df[4][i],negative_R=line_df[5][i],negative_X=line_df[6][i],
                                        zero_R=line_df[7][i],zero_X=line_df[8][i],zero_half_B=line_df[10][i])
        
        if fault_con.fault_type == 0:
            for i in range(len(result_v)):
                ThreeFaultV.objects.create(Bus_No=result_v[0][i], Voltage_Mag=result_v[1][i], Voltage_Deg=result_v[2][i])
            for i in range(len(result_cur)):
                ThreeFaultI.objects.create(From_Bus=result_cur[0][i], To_Bus=result_cur[1][i],
                                            Current_Mag=result_cur[2][i], Current_Deg=result_cur[3][i])
        else:
            for i in range(len(result_v)):
                OtherFaultV.objects.create(Bus_No=result_v[0][i], Phase_A_Mag=result_v[1][i], Phase_A_Deg=result_v[2][i],
                                            Phase_B_Mag=result_v[3][i], Phase_B_Deg=result_v[4][i],Phase_C_Mag=result_v[5][i], Phase_C_Deg=result_v[6][i])
            for i in range(len(result_cur)):
                OtherFaultI.objects.create(From_Bus=result_cur[0][i], To_Bus=result_cur[1][i], Phase_A_Mag=result_cur[2][i], Phase_A_Deg=result_cur[3][i],
                                            Phase_B_Mag=result_cur[4][i], Phase_B_Deg=result_cur[5][i],Phase_C_Mag=result_cur[6][i], Phase_C_Deg=result_cur[7][i])
        return redirect('result')
    busdata = BusData.objects.all()
    linedata = LineData.objects.all().exclude(from_bus=0).exclude(to_bus=0)
    context ={'busdata':busdata,'linedata':linedata}
    return render(request, 'cal/fault_con.html', context=context)

def result(request):
    faultcon = FaultCondition.objects.get(to_find=True)
    faultbusdata=FaultBusData.objects.all()
    faultlinedata=FaultLineData.objects.all()
    threefaultv=ThreeFaultV.objects.all()
    threefaulti=ThreeFaultI.objects.all()
    otherfaultv=OtherFaultV.objects.all()
    otherfaulti=OtherFaultI.objects.all()
    context = {'faultbusdata':faultbusdata,'faultlinedata':faultlinedata,'threefaultv':threefaultv,'threefaulti':threefaulti,
                'otherfaultv':otherfaultv,'otherfaulti':otherfaulti, 'faultcon':faultcon}
    return render(request, 'cal/fault_result.html',context=context)



def bus_scaling(bus_df, basemva):
    bus_df.iloc[:, 3:9] /= basemva
    return bus_df

def flow_y_bus(line_d):
    j = complex(0, 1)
    fb = line_d.iloc[:, 0]
    tb = line_d.iloc[:, 1]
    r = line_d.iloc[:, 2]
    x = line_d.iloc[:, 3]
    half_b = j * line_d.iloc[:, 4]
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
            bus[fb[i] - 1, fb[i] - 1] += y[i] + half_b[i]
            bus[tb[i] - 1, tb[i] - 1] += y[i] + half_b[i]
    return bus

def gauss_flow_test(line_d, bus_d):
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
    return bus_d, repeat

def fault_line_data_scaling(line_df, fault_type):
    if fault_type > 0:
        fb = line_df.iloc[:, 0]
        con_num = len(fb)
        line_df.iloc[:,8] += 3 * line_df.iloc[:, 9]
        append_count = 0
        for i in range(con_num):
            if line_df[11][i] == 1:
                line_df.loc[con_num + append_count] = [line_df[0][i], 0, 0, 0, line_df[4][i], 0, 0,
                                                        line_df[7][i], line_df[8][i], line_df[9][i],
                                                        line_df[10][i], line_df[11][i]]
                append_count += 1
                line_df[7][i] = 0
                line_df[8][i] = 0
                line_df[9][i] = 0
            if line_df[11][i] == 2:
                line_df.loc[con_num + append_count] = [0, line_df[1][i], 0, 0, line_df[4][i], 0, 0,
                                                        line_df[7][i], line_df[8][i], line_df[9][i],
                                                        line_df[10][i], line_df[11][i]]
                append_count += 1
                line_df[7][i] = 0
                line_df[8][i] = 0
                line_df[9][i] = 0
            if line_df[11][i] >= 3:
                line_df[7][i] = 0
                line_df[8][i] = 0
                line_df[9][i] = 0
    line_df = line_df.astype({0: 'int'})
    line_df = line_df.astype({1: 'int'})
    return line_df

def line_sliding_scaling(line_d, voltage, fault_bus_1, fault_bus_2, percent):
    fb = line_d.iloc[:, 0]
    tb = line_d.iloc[:, 1]
    con_num = len(fb)
    bus_size = max(max(fb), max(tb))
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
    voltage.loc[bus_size] = voltage[fault_bus_1 - 1] * percent + voltage[fault_bus_2 - 1] * (1-percent)
    fault_loc = bus_size + 1
    line_d = line_d.astype({0: 'int'})
    line_d = line_d.astype({1: 'int'})
    return line_d, voltage, fault_loc

def y_bus(line_d):
    j = complex(0, 1)
    fb = line_d.iloc[:, 0]
    tb = line_d.iloc[:, 1]
    r = line_d.iloc[:, 2]
    x = line_d.iloc[:, 3]
    half_b = j * line_d.iloc[:, 4]
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
            bus[fb[i] - 1, fb[i] - 1] += y[i] + half_b[i]
            bus[tb[i] - 1, tb[i] - 1] += y[i] + half_b[i]
    return bus


def zbus(line_d):
    return np.linalg.inv(y_bus(line_d))


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
    return np.linalg.inv(bus)


def fault_select(bus_voltage, line_d, bus_d, fault_location, fault_impedance, fault_type,
                half_b_consider, is_bus_load):
    if fault_type == 0:
        return three_phase_fault(bus_voltage, line_d, bus_d, fault_location, fault_impedance,
                                half_b_consider, is_bus_load)
    else:
        return unbalanced_fault(bus_voltage, line_d, bus_d, fault_location, fault_impedance, fault_type,
                                half_b_consider, is_bus_load)

def three_phase_fault(bus_voltage, line_d, bus_d, fault_location, fault_impedance,
                        half_b_consider, is_bus_load):
    j = complex(0, 1)
    fb = line_d.iloc[:, 0]
    tb = line_d.iloc[:, 1]
    r = line_d.iloc[:, 2]
    x = line_d.iloc[:, 3]
    half_b = line_d.iloc[:, 4]

    if not half_b_consider:
        half_b *= 0

    three_phase_d = pd.concat([fb, tb, r, x, half_b], axis=1)
    z = r + j * x
    con_num = len(fb)
    bus_size = max(max(fb), max(tb))
    if is_bus_load:
        fault_bus = load_zbus(three_phase_d, bus_d)
    else:
        fault_bus = zbus(three_phase_d)
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
    return fault_bus_voltage, fault_line_current


def unbalanced_fault(bus_voltage, line_d, bus_d, fault_location, fault_impedance, fault_type,
                    half_b_consider, is_bus_load):
    j = complex(0, 1)
    fb = line_d.iloc[:, 0]
    tb = line_d.iloc[:, 1]
    positive_r = line_d.iloc[:, 2]
    positive_x = line_d.iloc[:, 3]
    half_b = line_d.iloc[:, 4]
    negative_r = line_d.iloc[:, 5]
    negative_x = line_d.iloc[:, 6]
    zero_r = line_d.iloc[:, 7]
    zero_x = line_d.iloc[:, 8]
    zero_half_b = line_d.iloc[:, 10]

    con_num = len(fb)
    bus_size = max(max(fb), max(tb))

    positive_z = positive_r + j * positive_x
    negative_z = negative_r + j * negative_x
    zero_z = zero_r + j * zero_x

    if not half_b_consider:
        half_b *= 0
    if is_bus_load:
        positive_fault_bus = df_to_load_zbus(fb, tb, positive_r, positive_x, half_b, bus_d)
        negative_fault_bus = df_to_load_zbus(fb, tb, negative_r, negative_x, half_b, bus_d)
        zero_fault_bus = df_to_load_zbus(fb, tb, zero_r, zero_x, zero_half_b, bus_d)
    else:
        positive_fault_bus = df_to_zbus(fb, tb, positive_r, positive_x, half_b)
        negative_fault_bus = df_to_zbus(fb, tb, negative_r, negative_x, half_b)
        zero_fault_bus = df_to_zbus(fb, tb, zero_r, zero_x, zero_half_b)
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

    for i in range(con_num):
        symmetrical_components = \
            symmetrical_component_fault_current(fb, tb, bus_voltage, symmetrical_fault_bus_voltage,
                                                        positive_z, negative_z, zero_z, i)
        fault_line_current[i, :] = np.transpose(a_matrix @ symmetrical_components)
    fault_line_current[con_num, :] = np.transpose(fault_phase_current)

    return fault_bus_voltage, fault_line_current

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


def df_to_zbus(fb, tb, r, x, half_b):
    df = pd.concat([fb, tb, r, x, half_b], axis=1)
    return zbus(df)


def df_to_load_zbus(fb, tb, r, x, half_b, bus_d):
    df = pd.concat([fb, tb, r, x, half_b], axis=1)
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

def after_fault_scaling(line_df, bus_df, voltage_d, current_d, fault_loc, fault_type):
    fb = line_df.iloc[:, 0]
    tb = line_df.iloc[:, 1]
    con_num = len(fb)
    current_d = np.round(current_d, 5)
    voltage_d = np.round(voltage_d, 5)
    bus_num = bus_df.iloc[:, 0]
    if fault_type == 0:
        frame_current_mag = pd.DataFrame(np.abs(current_d))
        frame_current_ang = pd.DataFrame(np.angle(current_d, deg=True))
        frame_current_d = pd.concat([fb, tb, frame_current_mag, frame_current_ang], axis=1)
        frame_voltage_mag = pd.DataFrame(np.abs(voltage_d))
        frame_voltage_ang = pd.DataFrame(np.angle(voltage_d, deg=True))
        frame_voltage_d = pd.concat([bus_num, frame_voltage_mag, frame_voltage_ang], axis=1)
        frame_current_d.columns = [0, 1, 2, 3]
        frame_voltage_d.columns = [0, 1, 2]
    else:
        frame_current_mag_a = pd.DataFrame(np.abs(current_d[:, 0]))
        frame_current_ang_a = pd.DataFrame(np.angle(current_d[:, 0], deg=True))
        frame_current_mag_b = pd.DataFrame(np.abs(current_d[:, 1]))
        frame_current_ang_b = pd.DataFrame(np.angle(current_d[:, 1], deg=True))
        frame_current_mag_c = pd.DataFrame(np.abs(current_d[:, 2]))
        frame_current_ang_c = pd.DataFrame(np.angle(current_d[:, 2], deg=True))
        frame_current_d = pd.concat([fb, tb, frame_current_mag_a, frame_current_ang_a, frame_current_mag_b,
                                    frame_current_ang_b, frame_current_mag_c, frame_current_ang_c], axis=1)
        frame_voltage_mag_a = pd.DataFrame(np.abs(voltage_d[:, 0]))
        frame_voltage_ang_a = pd.DataFrame(np.angle(voltage_d[:, 0], deg=True))
        frame_voltage_mag_b = pd.DataFrame(np.abs(voltage_d[:, 1]))
        frame_voltage_ang_b = pd.DataFrame(np.angle(voltage_d[:, 1], deg=True))
        frame_voltage_mag_c = pd.DataFrame(np.abs(voltage_d[:, 2]))
        frame_voltage_ang_c = pd.DataFrame(np.angle(voltage_d[:, 2], deg=True))
        frame_voltage_d = pd.concat([bus_num, frame_voltage_mag_a, frame_voltage_ang_a, frame_voltage_mag_b,
                                    frame_voltage_ang_b, frame_voltage_mag_c, frame_voltage_ang_c], axis=1)
        frame_current_d.columns = [0, 1, 2, 3, 4, 5, 6, 7]
        frame_voltage_d.columns = [0, 1, 2, 3, 4, 5, 6]
    bus_num = frame_voltage_d.iloc[:, 0]
    b_n = len(bus_num)
    frame_voltage_d.iloc[b_n - 1,0] = b_n
    frame_current_d.iloc[con_num, 0] = fault_loc
    frame_current_d.iloc[con_num, 1] = -1
    return frame_voltage_d, frame_current_d
