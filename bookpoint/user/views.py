
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password

from .models import Role, User
from utils.validators import email_validator, pass_validator


def login(request: HttpRequest):
    if request.method == "GET":
        if request.COOKIES.get('email') is not None:
            return redirect('/core/home')
        
        return render(request, 'user/login.html')

    email = request.POST.get('email')
    password = request.POST.get('password')
    
    user = User.objects.filter(email=email)
    if user.count() == 0:
        return render(request, 'user/login.html', {
            'error': 'Wrong email or password'
        })

    if not check_password(password, user.get().password_hash):
        return render(request, 'user/login.html', {
            'error': 'Wrong email or password'
        })
    
    # Cookie
    response = redirect("/core/home")
    response.set_cookie('email', email)
    
    return response


def signup(request: HttpRequest):
    if request.method == "GET":
        if request.COOKIES.get('email') is not None:
            return redirect('/core/home')
        
        return render(request, 'user/signup.html')

    email = request.POST.get('email')
    password = request.POST.get('password')
    confirmPassword = request.POST.get('confirm-password')
    
    if password != confirmPassword:
        return render(request, 'user/signup.html', {
            'error': 'Passwords do no match'
        })
        

    is_email_valid = email_validator.validate(email)
    if not is_email_valid:
        return render(request, 'user/signup.html', {
            'error': 'Email is invalid'
        })

    is_password_valid = pass_validator.validate(password)
    if not is_password_valid:
        return render(request, 'user/signup.html', {
            'error': "Password must be more than 8 characters and must contain at least one capital, small, number, and special character(s)"
        })
    
    existing_email = User.objects.filter(email=email)
    if existing_email.count() > 0:
        return render(request, 'user/signup.html', {
            'error': "Email is already taken"
        })

    customer_role = Role.objects.get(name="Customer")
    hashsed_password = make_password(password)

    # insert
    User.objects.create(
        email=email,
        password_hash=hashsed_password,
        role=customer_role
    )

    return redirect('/user/login')


def logout(request: HttpRequest):
    response = redirect('/user/login')
    response.delete_cookie('email')
    
    return response    



