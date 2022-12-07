from django.shortcuts import render
from .forms import loginPostForm


# Create your views here.

def ownerLogin(request):
    if request.method == 'POST':
        return render(request, 'findPassword.html')
    else:
        form = loginPostForm()
        return render(request, 'ownerLogin.html', {'form': form, 'flg': False})


def findPassword(request):
    return render(request, 'findPassword.html')
