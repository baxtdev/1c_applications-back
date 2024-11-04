from django.shortcuts import render

# Create your views here.

def create_report(request):
    return render(request, 'create_report.html')

def index(request):
    return render(request, 'index.html')