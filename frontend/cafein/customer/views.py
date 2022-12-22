
from django.shortcuts import redirect, render

from customer.forms import customerPostForm


def customerHome(request):
    if request.session.get('user'):
        return render(request, 'customerHome.html')
    else:
        return redirect('/')


def signup(request):
    if not(request.session.get('user')):
        if request.method == 'POST':
            form = customerPostForm(request.POST, request.FILES)
            if form.is_valid():
                if not form.check_email():
                    return render_with_error(request, 'signup.html', form, ['email'])
                if not (form.check_password1() and form.check_password()):
                    return render_with_error(request, 'signup.html', form, ['password'])
                if not form.check_phone():
                    return render_with_error(request, 'signup.html', form, ['phone'])
                
                form.save()
                # Save 성공시에는 Redirect
                request.session['user'] = request.POST.get('email')
                request.session['is_owner'] = False
                return redirect('/customer/home')
        else:
            form = customerPostForm()
            return render(request, 'signup.html', {'form': form})
    return redirect('/')

def render_with_error(request, html, form, error_type):
    error_flg = {}
    for error in error_type:
        error_flg[error] = True
    return render(request, html, {'form': form, 'error_flg': error_flg})