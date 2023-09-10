from django import forms

class ConditonForm(forms.Form):
    is_flow_choices = [(True,'조류 계산'),
                        (False,'사용자 입력'),
                        ]
    fault_type_choices = [(0,'3상 고장(balanced fault)'),
                        (1,'1선 지락(single line to ground fault)'),
                        (2,'선간 단락(line to line fault)'),
                        (3,'2선 지락(double line to ground fault)'),
                        ]
    bus_choice = [(True,'BUS에서 고장'),
                (False,'line에서 고장'),
                ]
    basemva = forms.IntegerField()
    is_flow = forms.ChoiceField(widget=forms.RadioSelect,choices=is_flow_choices)
    fault_type = forms.ChoiceField(widget=forms.RadioSelect,choices=fault_type_choices)
    is_bus_fault = forms.ChoiceField(widget=forms.RadioSelect,choices=bus_choice)
    fault_bus = forms.IntegerField()
    fault_line_1 = forms.IntegerField()
    fault_line_2 = forms.IntegerField()
    line_percentage = forms.IntegerField()
    impedence_R = forms.FloatField()
    impedence_X = forms.FloatField()
    is_shunt = forms.BooleanField()
    is_load_effect = forms.BooleanField()