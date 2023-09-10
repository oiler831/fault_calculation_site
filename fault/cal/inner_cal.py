import pandas as pd
import numpy as np
from flow_calculation import gauss_flow_test
import fault_calculation
import scaling
from models import FaultCondition, ExcelFile, ThreeFaultV, ThreeFaultI, OtherFaultI, OtherFaultV, FaultBusData, FaultLineData

def inner_cal():
    j = complex(0, 1)
    file = ExcelFile.objects.get(find_file=True)
    fault_con = FaultCondition.objects.get(to_find=True)
    bus_df = pd.read_excel(file.file.path,sheet_name=0, header=None) 
    line_df = pd.read_excel(file.file.path,sheet_name=1, header=None) 
    bus_df = scaling.bus_scaling(bus_df, fault_con.basemva)
    if fault_con.is_flow:
        bus_df, repeat_count = gauss_flow_test(line_df, bus_df)
    initial_bus_voltage = bus_df.iloc[:, 1] * np.exp(j * np.deg2rad(bus_df.iloc[:, 2])) 
    line_df = scaling.fault_line_data_scaling(line_df, fault_con.fault_type) 
    fault_impedence = fault_con.impedence_R + j * fault_con.impedence_X
    if fault_con.is_bus_fault:
        fault_loc = fault_con.fault_bus
    else:
        line_df, initial_bus_voltage, fault_loc = \
            scaling.line_sliding_scaling(line_df, initial_bus_voltage, fault_con.fault_line_1, fault_con.fault_line_2, fault_con.line_percentage/100)
    result_v, result_cur = fault_calculation.fault_select(initial_bus_voltage, line_df, bus_df,
                                                        fault_loc, fault_impedence, fault_con.fault_type,
                                                        fault_con.is_shunt, fault_con.is_load_effect)
    result_v, result_cur = scaling.after_fault_scaling(line_df, bus_df, result_v, result_cur, fault_loc, fault_con.fault_type)
    bus_df = scaling.after_flow_scaling(bus_df, fault_con.basemva)

    for i in range(len(bus_df)):
        FaultBusData.objects.create(Bus_No=bus_df[i][0], Bus_Code=bus_df[i][1], Voltage_Mag=bus_df[i][2], Voltage_Deg=bus_df[i][3],
                                    Generator_MW=bus_df[i][4],Generator_Mvar=bus_df[i][5],Load_MW=bus_df[i][6],Load_Mvar=bus_df[i][7])

    for i in range(len(line_df)):
        FaultLineData.objects.create(From_Bus=line_df[i][0], To_Bus=line_df[i][1], R=line_df[i][2], X=line_df[i][3],
                                    half_B=line_df[i][4],negative_R=line_df[i][5],negative_X=line_df[i][6],zero_R=line_df[i][7],
                                    zero_X=line_df[i][8],zero_half_B=line_df[i][9])
    if fault_con.fault_type == 0:
        for i in range(len(result_v)):
            ThreeFaultV.objects.create(Bus_No=result_v[i][0], Voltage_Mag=result_v[i][1], Voltage_Deg=result_v[i][2])
        for i in range(len(result_cur)):
            ThreeFaultI.objects.create(From_Bus=result_cur[i][0], To_Bus=result_cur[i][1],
                                        Current_Mag=result_cur[i][2], Current_Deg=result_cur[i][3])
    else:
        for i in range(len(result_v)):
            OtherFaultV.objects.create(Bus_No=result_v[i][0], Phase_A_Mag=result_v[i][1], Phase_A_Deg=result_v[i][2],
                                        Phase_B_Mag=result_v[i][3], Phase_B_Deg=result_v[i][4],Phase_C_Mag=result_v[i][5], Phase_C_Deg=result_v[i][6])
        for i in range(len(result_cur)):
            OtherFaultI.objects.create(From_Bus=result_cur[i][0], To_Bus=result_cur[i][1], Phase_A_Mag=result_cur[i][2], Phase_A_Deg=result_cur[i][3],
                                        Phase_B_Mag=result_cur[i][4], Phase_B_Deg=result_cur[i][5],Phase_C_Mag=result_cur[i][6], Phase_C_Deg=result_cur[i][7])
    
