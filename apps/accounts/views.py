from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm
from .models import User

# Create your views here.


def register(request):
    form = CustomUserCreationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('accounts:register')

    context = {'form': form}

    return render(request, 'accounts/register.html', context)


def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    return 1
