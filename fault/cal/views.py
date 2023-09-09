from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'cal/main.html')

def manual(request):
    return render(request,'cal/main.html')