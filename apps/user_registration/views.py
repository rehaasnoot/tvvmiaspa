from django.shortcuts import render
#from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
 
def registerUser(response):
    if "POST" == response.method:
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserCreationForm()
    return render(response, 'register.html', { "form": form })