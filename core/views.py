from .models import Customer
from .functions import check_password
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.utils import IntegrityError, DataError
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
def IndexView(request):
    return render(request, 'core/index.html')

def LoginView(request):
    '''the code that runs when requesting the login page'''

    if request.method == 'POST':
        '''check and authenticate credentials'''
        
        # fetch client input from http request 
        username = request.POST['uname']
        password = request.POST['pswd']
        
        #authenticate user:
        user = authenticate(username=username, password=password)
        if not user:
            return render(request, 'core/login.html',{'error': 'Sorry, incorrect username or password'})
        else:
            login(request, user)

        #redirect to index page
        return HttpResponseRedirect(reverse('core:index'))
    
    else: #request.method == 'GET':
        return render(request, 'core/login.html', {})

    
def RegisterView(request):
    '''the code that runs when requesting the register page'''

    if request.method == 'POST':
    
        # fetch client input from http request
        username = request.POST['uname']
        password = request.POST['pswd']
        email = request.POST['email']
        phone = request.POST['phone']

        # check password rules
        error = check_password(password)
        if error:
            return render(request, 'core/register.html', {'error':error})
        
        # create user and assign to customer group
        User = get_user_model()
        customer_group = Group.objects.get(name='customer')
        try:
            user = User.objects.create_user(username = username, password = password, email = email)
            user.groups.add(customer_group)
        except (IntegrityError, DataError ) as e:
            return render(request, 'core/login.html', {'error':e})
        
        # create customer entry and link to user
        customer = Customer.objects.create(account = user, phone = phone)
        customer.save()
        #attach user to request, and redirect to index page
        login(request, user)
        return HttpResponseRedirect(reverse('core:index'))
    
    else: #request.method == 'GET':
        return render(request, 'core/register.html', {})

        



        
        
        






            
            
        

        
        

        

        
        