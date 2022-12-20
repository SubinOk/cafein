
from django.shortcuts import redirect, render


def customerHome(request):
    if request.session.get('user'):
        return render(request, 'customerHome.html')
    else:
        return redirect('/')


