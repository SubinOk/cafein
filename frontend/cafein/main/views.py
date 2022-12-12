from django.shortcuts import render

# Create your views here.
def mainPage(request):
    return render(request, 'mainPage.html')

def login(request):
    return render(request, 'login.html')
