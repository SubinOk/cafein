from django.shortcuts import render


# Create your views here.

def ownerLogin(request):
    return render(request, 'ownerLogin.html')


def findPassword(request):
    return render(request, 'findPassword.html')
