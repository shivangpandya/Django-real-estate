from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from contacts.models import Contact

# Create your views here.

def register(request):
    if request.method == 'POST':
        #Get form values
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        #Check if passwords match
        if password == password2:
            #Check username
            if User.objects.filter(username=username).exists():
                messages.error(request,'That username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'That email is used')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username , password = password , email=email,first_name=first_name,last_name=last_name)

            #Login after register
            user.save()
            messages.success(request,'You are now regsitred and can log in')
            return redirect('login')


        else:
            messages.error( request , 'Passwords do not match')
            return redirect('register')


        #Register user
        
    else:
        return render(request , 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        #Login user
        username = request.POST.get('username')
        password = request.POST.get('password')

        user=auth.authenticate(username = username , password = password)

        if user is not None:
            auth.login(request,user)
            messages.success(request,'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid username or password')
            return redirect('login')

            

    else:    
        return render(request , 'accounts/login.html')



def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'You are now logged out')
        return redirect('index')
    

def dashboard(request):
    user_cotacts = Contacts.objects.order_by('-contact_date').filter(user_id = request.user.id)

    context = {
        'contacts':user_contacts
    }
    return render(request , 'accounts/dashboard.html')
