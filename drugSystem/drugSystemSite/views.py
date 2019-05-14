from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'index.html',)

def goToDrugsInteraction(request):
    return render(request, 'drugsInteraction.html', )

def goToDiagnose(request):
    return render(request, 'diagnose.html', )

def goToIllnessSearch(request):
    return render(request, 'illnessSearch.html', )

def goToDrugSearch(request):
    return render(request, 'drugSearch.html', )
