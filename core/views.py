from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .functions import check_password


# Create your views here.
def IndexView(request):
    return render(request, 'core/index.html')

def LoginView(request):
    if request.method == 'GET':
        return render(request, 'core/login.html')

    else: #request.method == 'POST'
        username = request.POST['uname']
        password = request.POST['pswd']

        #check password rules
        error_message = check_password(password)
        if error_message:
            return render(request, 'core/login.html', {'error_message':error_message})

        #authenticate user:
        user = authenticate(username=username, password=password)
        if not user:
            return render(request, 'core/login.html', {'error_message': 'Sorry, incorrect username or password'})
        else:
            login(request, user)

        return HttpResponseRedirect(reverse('core:index'))
            
            
        

        
        

        

        
        