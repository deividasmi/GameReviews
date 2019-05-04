from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created succesfully.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'Users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, f'Account updated succesfully.')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form' : user_form
    }
    return render(request, 'Users/profile.html', context)