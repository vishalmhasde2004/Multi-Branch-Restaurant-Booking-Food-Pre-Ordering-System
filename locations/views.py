from django.shortcuts import render

# Create your views here.

def locations(request):
    return render(request, 'locations/locations.html')

def surat(request):
    return render(request, 'locations/surat.html')

def delhi(request):
    return render(request, 'locations/delhi.html')

def pune(request):
    return render(request, 'locations/pune.html')