from django.shortcuts import redirect, render

# Create your views here.
def mainPage(request):
    if request.session.get('user'):
        return redirect('/owner/home')
    return render(request, 'mainPage.html')

def login(request):
    return render(request, 'login.html')
