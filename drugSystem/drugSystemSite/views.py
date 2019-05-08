from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'index.html',)


def drugs(request):
    return render(request, 'drugsrelation.html', )