from django.shortcuts import render

# Create your views here.
def ownerlogin(request):
    return render(request, 'ownerlogin.html')
