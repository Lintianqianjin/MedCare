from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'drugSystemSite/index.html', )

def goToDrugsInteraction(request):
    return render(request, 'drugSystemSite/drugsInteraction.html', )

def goToDiagnose(request):
    return render(request, 'drugSystemSite/diagnose.html', )

def goToIllnessSearch(request):
    return render(request, 'drugSystemSite/illnessSearch.html', )

def goToDrugSearch(request):
    return render(request, 'drugSystemSite/drugSearch.html', )
