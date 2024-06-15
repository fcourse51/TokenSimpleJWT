from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import SignupForm, LoginForm, ResetPasswordForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
# Home page
@login_required
def index(request):
    user = request.user
    context = {
        'firstname': user.first_name,
        'lastname': user.last_name,
        'email': user.email
    }
    return render(request, 'index.html', context)

# signup page
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
       
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('home')
            else:
                print("Incorrect credentials !!")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')

# reset password
def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
       
        if form.is_valid():
            username = form.cleaned_data['username']
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']

            # Check if the user exists
            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                error_message = "User does not exist"
                return render(request, 'reset_password.html', {'error_message': error_message})
        
            if current_password == new_password:
                error_message = "Old and new password should be different !!"
                return render(request, 'reset_password.html', {'error_message': error_message})

            user = authenticate(request, username=username, password=current_password)
            if user:
                # Change the password
                user.set_password(new_password)
                user.save()
                success_message = "Password successfully changed"
                messages.success(request, success_message)
                return redirect('login') 
                # success_message = "Password successfully changed"
                # return render(request, 'reset_password.html', {'success_message': success_message})
            else:
                error_message = "Incorrect credentials !!"
                return render(request, 'reset_password.html', {'error_message': error_message})
        else:
            form = ResetPasswordForm()
    else:
        form = ResetPasswordForm()

    return render(request, 'reset_password.html', {'form': form})
